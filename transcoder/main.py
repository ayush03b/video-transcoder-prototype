import os

from pathlib import Path
import subprocess
import boto3
from secret_keys import SecretKeys

secret_keys = SecretKeys()

class Transcoder:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            region_name=secret_keys.AWS_REGION,
            aws_access_key_id=secret_keys.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=secret_keys.AWS_SECRET_ACCESS_KEY
        )


    """
    Returns the appropriate type of info on how would browsers should view the file
    """
    def _get_content_type(self, file_path: str):
        if file_path.endswith(".m3u8"):
            return "application/vnd.apple.mpegurl"
        elif file_path.endswith(".ts"):
            return "video/MP2T"
        elif file_path.endswith(".mpd"):
            return "application/dash+xml"
        elif file_path.endswith(".m4s"):
            return "video/mp4"
    
    """    
    Downloads the file to local path i.e. /tmp/workspace/input
    """
    def download_video(self, local_path):
        print()
        print("============================LOGS========================")
        print("Trying to download from bucket:", secret_keys.S3_BUCKET)
        print("With key:", secret_keys.S3_KEY)
        self.s3_client.download_file(
            secret_keys.S3_BUCKET,
            secret_keys.S3_KEY,
            local_path,
        )   
    
    """
    Transcoding and Segmentation of the raw video from s3
    """
    def transcode_videos(self, input_path, output_dir):
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-filter_complex",
            "[0:v]split=3[v1][v2][v3];"
            "[v1]scale=640:360:flags=fast_bilinear[360p];"
            "[v2]scale=1280:720:flags=fast_bilinear[720p];"
            "[v3]scale=1920:1080:flags=fast_bilinear[1080p]",
            
            # Map video streams
            "-map", "[360p]",
            "-map", "[720p]",
            "-map", "[1080p]",

            # Encoding settings
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-profile:v", "high",
            "-level:v", "4.1",
            "-g", "48",
            "-keyint_min", "48",
            "-sc_threshold", "0",

            # Bitrates
            "-b:v:0", "1000k",
            "-b:v:1", "4000k",
            "-b:v:2", "8000k",

            # HLS specific settings
            "-f", "hls",
            "-hls_time", "6",
            "-hls_playlist_type", "vod",
            "-hls_flags", "independent_segments",
            "-hls_segment_type", "mpegts",
            "-hls_list_size", "0",
            "-master_pl_name", "master.m3u8",
            "-var_stream_map", "v:0 v:1 v:2",
            "-hls_segment_filename", f"{output_dir}/%v/segment_%03d.ts",

            # Output playlists per resolution
            f"{output_dir}/%v/playlist.m3u8",
        ]

        # subprocess lets you run shell commands from python code and returns 0 if run sucessfully
        process = subprocess.run(cmd)

        # if crashes log the error
        if process.returncode != 0:
            print(process.stderr)
            raise Exception("Transcoding failed!")
        

    def upload_files(self, prefix: str, local_dir):
        # traverses the folders and files and creates path strings 
        for root, _, files in os.walk(local_dir):
            for file in files:
                """
                creates file path like : ideos/boom123/0/segment_000.ts which will be then interpreted 
                like virtual folders in s3
                """
                local_path = os.path.join(root, file)
                """
                removes the /tmp/workspace/ from the file name and attaches it to the s3 prefix 
                that creates s3 file path like /videos/xyz/abc
                """
                s3_key = f"{prefix}/{os.path.relpath(local_path, local_dir)}"
                self.s3_client.upload_file(
                    local_path, 
                    secret_keys.S3_PROCESSED_VIDEOS_BUCKET,
                    s3_key,
                    ExtraArgs={
                        "ACL" : "public-read",
                        "ContentType" : self._get_content_type(local_path),
                    },
                )


    """
    Main function that runs the whole Download -> Segment -> Transcode -> Upload process
    """
    def process_video(self):
        print("=== VideoTranscoder Service Starting ===")
        print()
        print("=========================debug logs========================")
        print("ENV S3_BUCKET:", os.environ.get("S3_BUCKET"))
        print("ENV S3_KEY:", os.environ.get("S3_KEY"))

        # creates a temporary path named - /tmp/workspace
        word_dir = Path("/tmp/workspace")

        # Makes sure that this path exists but doesn't throw error if it doesn't exist
        word_dir.mkdir(exist_ok=True)

        # create input path where all uploaded raw s3 files will be stored on disk on this path : /tmp/workspace/input.mp4
        # ⚠️ The name input.mp4 is hardcoded, so every file gets saved with this name locally before processing
        input_path = word_dir / "input.mp4"

        # path for transcoded videos segments (directory not a file)
        output_path = word_dir / "output"

        # path existence check
        output_path.mkdir(exist_ok=True)

        try:
            self.download_video(input_path)
            self.transcode_videos(str(input_path), str(output_path))
            self.upload_files(secret_keys.S3_KEY, str(output_path))
        finally:
            # Deletes the input video file /tmp/workspace/input.mp4 after processing
            if input_path.exists():
                input_path.unlink()
            if output_path.exists():
                import shutil
                shutil.rmtree(str(output_path))

Transcoder().process_video()