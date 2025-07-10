# 🎞️ Video Transcoder API *PROTOTYPE
A high-performance, scalable video transcoding pipeline built using FastAPI, S3, SQS, and ECS Fargate, designed to process and convert videos on demand. Think of it as your own mini-YouTube backend transcoder. Just upload a video and let the system handle the rest — automatic format conversion, async queue processing, and robust cloud-native architecture.

✅ Upload videos via presigned S3 URLs

✅ Async video processing using SQS + ECS Fargate

✅ Video consumer service in Python

✅ Transcodes videos using FFmpeg

✅ Uploads the final video to an S3 videos/ directory

✅ Handles status updates and retries

```
| Component        | Tech                          |
| ---------------- | ----------------------------- |
| API Gateway      | FastAPI                       |
| Messaging Queue  | AWS SQS                       |
| Object Storage   | AWS S3                        |
| Compute Backend  | AWS ECS Fargate               |
| Video Processing | FFmpeg (inside ECS container) |
| Language         | Python 3.x                    |
| Infrastructure   | Docker + ECS Task Definitions |
```

```
.
├── client
│   └── s3-uploader
│       ├── eslint.config.js
│       ├── index.html
│       ├── package-lock.json
│       ├── package.json
│       ├── public
│       │   └── vite.svg
│       ├── README.md
│       ├── src
│       │   ├── App.css
│       │   ├── App.jsx
│       │   ├── assets
│       │   │   └── react.svg
│       │   ├── index.css
│       │   └── main.jsx
│       └── vite.config.js
├── consumer
│   ├── main.py
│   ├── requirements.txt
│   └── secret_keys.py
├── README.md
├── server
│   ├── api
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── s3_client.py
│   ├── core
│   │   ├── __init__.py
│   │   └── config.py
│   ├── db_setup.py
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── main.py
│   ├── models.py
│   └── requirements.txt
└── transcoder
    ├── Dockerfile
    ├── main.py
    ├── requirements.txt
    └── secret_keys.py

```

> Cant test the project locally cuz I removed all the creds from the env file
