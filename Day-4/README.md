# Dockerized Flask Application with Jenkins CI Pipeline

## Project Overview.

This project demonstrates how to build and deploy a Flask application using:

- Docker
- Jenkins Pipeline
- GitHub Webhook
- AWS EC2

The goal of this project is to automate the application deployment process using Jenkins CI/CD pipeline and Docker containerization.

Whenever code is pushed to GitHub, Jenkins automatically:

1. Pulls latest code
2. Builds Docker image
3. Runs Docker container
4. Deploys Flask application

---

# Architecture

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
GitHub Webhook
    │
    ▼
Jenkins Pipeline
    │
    ▼
Docker Build
    │
    ▼
Docker Container
    │
    ▼
Flask Application
```

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python Flask | Web Application |
| Docker | Containerization |
| Jenkins | CI/CD Automation |
| GitHub | Source Code Management |
| AWS EC2 | Hosting Jenkins & Docker |
| Linux | Server Environment |

---

# Project Structure

```text
dockerize-flask-jenkins/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
└── README.md
```

---

# Flask Application

## app.py

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Docker Flask App Running"

@app.route('/profile')
def profile():
    return "Profile Page"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

---

# Requirements File

## requirements.txt

```text
Flask==3.0.0
```

---

# Dockerfile

```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

# Jenkins Pipeline

## Jenkinsfile

```groovy
pipeline {
    agent any

    stages {

        stage('build docker image') {
            steps {
                sh 'docker build -t flask-app .'
            }
        }

        stage('run docker container') {
            steps {
                sh '''
                docker rm -f flask-container || true

                docker run -d -p 5000:5000 \
                --name flask-container flask-app
                '''
            }
        }
    }
}
```

---

# Jenkins Setup

## Install Java

```bash
sudo apt update

sudo apt install openjdk-17-jdk -y
```

---

# Install Jenkins

```bash
sudo apt install jenkins -y
```

Start Jenkins:

```bash
sudo systemctl enable jenkins

sudo systemctl start jenkins
```

---

# Install Docker

```bash
sudo apt install docker.io -y
```

Start Docker:

```bash
sudo systemctl enable docker

sudo systemctl start docker
```

---

# Configure Docker Permissions

Add Jenkins user to Docker group:

```bash
sudo usermod -aG docker jenkins
```

Restart services:

```bash
sudo systemctl restart docker

sudo systemctl restart jenkins
```

---

# GitHub Webhook Configuration

GitHub Webhook URL:

```text
http://<jenkins-public-ip>:8080/github-webhook/
```

Content Type:

```text
application/json
```

Events:

```text
Just the push event
```

---

# Pipeline Workflow

```text
Git Push
   ↓
GitHub Webhook Trigger
   ↓
Jenkins Pipeline Starts
   ↓
Docker Image Build
   ↓
Old Container Removed
   ↓
New Container Started
   ↓
Flask App Updated
```

---

# Build & Deployment Commands

## Build Docker Image

```bash
docker build -t flask-app .
```

---

# Run Docker Container

```bash
docker run -d -p 5000:5000 \
--name flask-container flask-app
```

---

# Verify Running Container

```bash
docker ps
```

---

# Check Container Logs

```bash
docker logs flask-container
```

---

# Access Application

```text
http://<public-ip>:5000
```

Profile Route:

```text
http://<public-ip>:5000/profile
```

---

# AWS Security Group Configuration

| Type | Port | Source |
|---|---|---|
| SSH | 22 | Your IP |
| Custom TCP | 8080 | 0.0.0.0/0 |
| Custom TCP | 5000 | 0.0.0.0/0 |

---

# Problems Faced & Solutions

---

## 1. Jenkins Pipeline Failed with `master` Branch Error

### Problem

```text
ERROR: Couldn't find any revision to build
```

### Root Cause

Jenkins tried to pull:

```text
origin/master
```

But GitHub repository used:

```text
main
```

### Solution

Changed Jenkins branch configuration:

```text
*/master → */main
```

---

## 2. Duplicate Git Clone in Jenkinsfile

### Problem

Pipeline failed during:

```text
stage('clone code')
```

### Root Cause

Declarative pipeline already performs:

```text
Checkout SCM
```

Manual `git` stage caused branch mismatch.

### Solution

Removed unnecessary clone stage from Jenkinsfile.

---

## 3. Docker Container Exited Immediately

### Problem

Container stopped instantly after running.

### Debug Command

```bash
docker logs flask-container
```

### Root Cause

Python syntax error inside Flask app.

---

## 4. Flask Syntax Error

### Problem

```python
def profile('/profile')
```

### Root Cause

Invalid Flask route syntax.

### Solution

Corrected route:

```python
@app.route('/profile')
def profile():
```

---

## 5. Git Rebase Conflict

### Problem

```text
CONFLICT (add/add): Merge conflict in README.md
```

### Root Cause

Different changes existed in local and remote repositories.

### Solution

Resolved conflict manually and continued rebase:

```bash
git add .

git rebase --continue
```

---

# Skills Learned

| Area | Concepts |
|---|---|
| Docker | Containerization |
| Jenkins | CI/CD Automation |
| GitHub | Version Control |
| Linux | Server Administration |
| DevOps | Automated Deployment |
| Debugging | Container Troubleshooting |
| AWS | EC2 Hosting |

---

# Real DevOps Concepts Learned

- CI/CD Pipeline
- Docker Container Lifecycle
- GitHub Webhooks
- Jenkins Declarative Pipeline
- Docker Logs Debugging
- Git Rebase Workflow
- Linux Permission Management
- Automated Deployment

---

# Important Commands Used

| Purpose | Command |
|---|---|
| Build image | `docker build -t flask-app .` |
| Run container | `docker run -d -p 5000:5000 flask-app` |
| View containers | `docker ps` |
| View logs | `docker logs flask-container` |
| Git pull rebase | `git pull --rebase origin main` |
| Push code | `git push origin main` |

---

# Interview Questions

| Question | Answer |
|---|---|
| Why use Jenkins with Docker? | Automate build and deployment |
| Why did container exit immediately? | Application crashed |
| Which command helps debug containers? | `docker logs` |
| What is webhook payload? | Data sent from GitHub to Jenkins |
| Why add Jenkins to Docker group? | Allow Jenkins to execute Docker commands |

---

# Future Improvements

- Add Docker Hub push stage
- Implement Docker Compose
- Deploy on Kubernetes
- Add Slack notifications
- Add automated testing stage
- Implement Blue-Green deployment

---

# Final Result

✅ Flask application containerized successfully  
✅ Jenkins CI pipeline configured successfully  
✅ GitHub webhook integrated successfully  
✅ Docker container deployed automatically  
✅ Application accessible through browser  
✅ CI/CD workflow automated successfully
