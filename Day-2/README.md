from pathlib import Path
import pypandoc

content = r"""
# README — Dockerized Flask Application

## Project Overview

This project demonstrates how to containerize a simple Flask application using Docker and push the Docker image to Docker Hub.

The application runs inside a Docker container and can be accessed through a web browser using the EC2 public IP and exposed container port.

---

# Architecture

Flask Application
        ↓
Docker Image
        ↓
Docker Container
        ↓
Docker Hub Registry

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python Flask | Web Application |
| Docker | Containerization |
| Docker Hub | Image Registry |
| Linux | Server Environment |
| AWS EC2 | Hosting Server |

---

# Project Structure

flask-app/
│
├── app.py
├── requirements.txt
├── Dockerfile
└── README.md

---

# Flask Application

## app.py

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Docker Flask App Running"

app.run(host='0.0.0.0', port=5000)

---

# Requirements File

## requirements.txt

Flask==3.0.0

---

# Dockerfile

FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

---

# Setup Instructions

## Step 1 — Clone Repository

git clone <your-github-repo-url>

cd flask-app

---

# Step 2 — Build Docker Image

docker build -t flask-app .

Verify image:

docker images

---

# Step 3 — Run Docker Container

docker run -d -p 5000:5000 --name flask-container flask-app

Verify container:

docker ps

---

# Step 4 — Access Application

Open browser:

http://<public-ip>:5000

Expected output:

Docker Flask App Running

---

# Docker Hub Integration

## Login to Docker Hub

docker login

---

# Tag Docker Image

docker tag flask-app <dockerhub-username>/flask-app:v1

---

# Push Image to Docker Hub

docker push <dockerhub-username>/flask-app:v1

---

# Pull Image from Docker Hub

docker pull <dockerhub-username>/flask-app:v1

---

# Run Pulled Image

docker run -d -p 5000:5000 <dockerhub-username>/flask-app:v1

---

# Common Docker Commands

| Purpose | Command |
|---|---|
| List running containers | docker ps |
| List images | docker images |
| View logs | docker logs <container> |
| Stop container | docker stop <container> |
| Remove container | docker rm <container> |
| Remove image | docker rmi <image> |

---

# Security Group Configuration

| Type | Port | Source |
|---|---|---|
| Custom TCP | 5000 | 0.0.0.0/0 |

---

# Skills Learned

| Area | Concepts |
|---|---|
| Docker | Image & Container Management |
| DevOps | Application Containerization |
| Linux | Docker CLI Commands |
| Networking | Port Mapping |
| Cloud | Hosting on EC2 |
| Registry | Docker Hub Integration |

---

# Future Improvements

- Add Docker Compose
- Use Nginx Reverse Proxy
- Implement CI/CD Pipeline
- Deploy using Kubernetes
- Add Persistent Storage

---

# Interview Questions

| Question | Answer |
|---|---|
| What is Docker? | Containerization platform |
| Difference between Image and Container? | Image is blueprint, container is running instance |
| Why expose ports in Docker? | To access application externally |
| What is Docker Hub? | Docker image registry |

---

# Expected Result

✅ Flask application runs inside Docker container
✅ Application accessible from browser
✅ Docker image pushed to Docker Hub
✅ Image reusable across environments
"""

output_path = "/mnt/data/docker_flask_readme.txt"
pypandoc.convert_text(
    content,
    'plain',
    format='md',
    outputfile=output_path,
    extra_args=['--standalone']
)

print(f"TXT file created at: {output_path}")

