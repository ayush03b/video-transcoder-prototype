import { useRef } from "react";

function App() {
  const fileInputRef = useRef();

  const handleUpload = async () => {
    const file = fileInputRef.current.files[0];
    if (!file) {
      alert("Pick a file first!");
      return;
    }

    // Step 1: Get presigned URL from FastAPI
    const res = await fetch(
      `http://localhost:8000/server/generate-presigned-url?file_name=${file.name}&file_type=${file.type}`
    );
    const { url, key } = await res.json();

    // Step 2: Upload file directly to S3 using PUT
    await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": file.type,
      },
      body: file,
    });

    alert("Upload successful! 🎉");
    console.log("Uploaded S3 key:", key);

    // Optional: Save metadata to FastAPI (skip if not needed)
    /*
    await fetch("http://localhost:8000/upload-metadata", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: "Cool video",
        description: "Uploaded via presigned URL",
        s3_key: key,
      }),
    });
    */
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>Upload a Video to S3</h2>
      <input type="file" accept="video/*" ref={fileInputRef} />
      <br /><br />
      <button onClick={handleUpload}>Upload to S3</button>
    </div>
  );
}

export default App;
