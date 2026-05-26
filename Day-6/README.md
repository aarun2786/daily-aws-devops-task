# Nginx Reverse Proxy for Docker Flask Application

## Project Overview

This project demonstrates how to deploy a Dockerized Flask application behind an Nginx Reverse Proxy on an AWS EC2 Ubuntu server.

The setup follows a real-world production-style architecture where:

- Nginx handles incoming client requests
- Nginx serves static frontend files
- Nginx forwards API requests to Flask backend
- Flask runs inside Docker container
- Redis runs inside Docker container
- Backend services remain isolated internally

This project helped in understanding:

- Reverse proxy architecture
- Docker networking
- Container communication
- Nginx configuration
- Backend isolation
- Production-style deployment patterns

---

# Architecture

```text
                 Browser
                     │
                     ▼
            Nginx Reverse Proxy
               (Port 80 Public)
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
 Static Frontend           API Requests
  index.html                 /api/*
                                  │
                                  ▼
                         Flask Docker Container
                                  │
                                  ▼
                           Redis Container
```

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Nginx | Reverse Proxy & Static Hosting |
| Docker | Containerization |
| Flask | Backend API |
| Redis | In-memory database |
| AWS EC2 | Cloud Infrastructure |
| Ubuntu Linux | Server Environment |

---

# Project Structure

```text
project/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── index.html
└── README.md
```

---

# Why Use Nginx Reverse Proxy?

Instead of exposing Flask directly:

```text
http://<public-ip>:5000
```

Nginx acts as a centralized entry point:

```text
http://<public-ip>
```

Benefits:

- Improved security
- Backend isolation
- Better performance
- Cleaner architecture
- Centralized routing
- Production-ready deployment

---

# Flask Backend Application

## app.py

```python
from flask import Flask, jsonify
import redis

app = Flask(__name__)

redis_client = redis.Redis(
    host='redis-server',
    port=6379,
    decode_responses=True
)

if not redis_client.exists('users'):
    redis_client.set('users', 0)

@app.route('/api/count')
def count():
    users = redis_client.get('users')
    return jsonify({"users": users})

@app.route('/api/join')
def join():
    users = redis_client.incr('users')
    return jsonify({"users": users})

@app.route('/api/leave')
def leave():
    users = redis_client.decr('users')
    return jsonify({"users": users})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

---

# Frontend Application

## index.html

```html
<script>

    const API = '/api';

    function hit(path) {

      fetch(API + path)
        .then(r => r.json())
        .then(d => document.getElementById('count').textContent = d.users);
    }

    hit('/count');

</script>
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

# requirements.txt

```text
Flask==3.0.0
redis==5.0.1
```

---

# Docker Networking Setup

---

# Step 1 — Create Docker Network

```bash
docker network create flask-network
```

---

# Step 2 — Run Redis Container

```bash
docker run -d \
--name redis-server \
--network flask-network \
redis
```

---

# Step 3 — Build Flask Image

```bash
docker build -t flask-app .
```

---

# Step 4 — Run Flask Container

```bash
docker run -d \
--name flask-container \
--network flask-network \
-p 5000:5000 \
flask-app
```

---

# Nginx Installation

```bash
sudo apt update

sudo apt install nginx -y
```

---

# Nginx Reverse Proxy Configuration

## flask-app.conf

```nginx
server {

    listen 80;

    server_name _;

    root /var/www/html;

    index index.html;

    location / {
        try_files $uri /index.html;
    }

    location /api/ {

        proxy_pass http://127.0.0.1:5000;

        proxy_set_header Host $host;

        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

# Enable Nginx Site

```bash
sudo ln -s /etc/nginx/sites-available/flask-app \
/etc/nginx/sites-enabled/
```

---

# Remove Default Site

```bash
sudo rm /etc/nginx/sites-enabled/default
```

---

# Test Nginx Configuration

```bash
sudo nginx -t
```

---

# Restart Nginx

```bash
sudo systemctl restart nginx
```

---

# Place Frontend File

```bash
sudo cp index.html /var/www/html/
```

---

# Access Application

```text
http://<public-ip>
```

---

# Request Flow

```text
Browser
   ↓
Nginx Reverse Proxy
   ├── Serves Frontend HTML
   └── Routes /api/* Requests
              ↓
         Flask Container
              ↓
           Redis Container
```

---

# Problems Faced During the Project

---

# 1. Nginx Returned "Not Found"

## Problem

Opening:

```text
http://<public-ip>
```

returned:

```text
Not Found
```

---

# Root Cause

Frontend HTML file was not properly configured in Nginx.

---

# Solution

Configured:

```nginx
root /var/www/html;

index index.html;
```

and copied frontend file into:

```text
/var/www/html/
```

---

# 2. Frontend Directly Exposed Backend IP

## Problem

Frontend JavaScript directly used backend IP:

```javascript
const API = 'http://18.x.x.x';
```

---

# Root Cause

Frontend bypassed reverse proxy architecture.

---

# Solution

Updated frontend API configuration:

```javascript
const API = '/api';
```

allowing Nginx to handle API routing internally.

---

# 3. API Requests Bypassed Reverse Proxy

## Problem

Browser communicated directly with Flask backend.

---

# Solution

Added reverse proxy configuration:

```nginx
location /api/ {

    proxy_pass http://127.0.0.1:5000;
}
```

---

# 4. Nginx Conflicting Server Name Warning

## Warning

```text
conflicting server name "_" on 0.0.0.0:80
```

---

# Root Cause

Ubuntu default Nginx site conflicted with custom configuration.

---

# Solution

Removed default Nginx site:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

---

# 5. Incorrect Reverse Proxy Backend Target

## Problem

Initially used:

```nginx
proxy_pass http://172.x.x.x:5000;
```

---

# Root Cause

Used EC2 private IP instead of localhost.

---

# Solution

Updated configuration:

```nginx
proxy_pass http://127.0.0.1:5000;
```

---

# 6. Redis Hostname Resolution Error

## Error

```text
Temporary failure in name resolution
```

---

# Root Cause

Used incorrect Redis hostname.

---

# Solution

Connected containers using Docker network and used Redis container name:

```python
host='redis-server'
```

---

# Docker Networking Learning

Learned that:

- Docker containers communicate using container names
- Docker networks provide internal DNS resolution
- `localhost` inside container refers only to that container

---

# Important Commands Used

| Purpose | Command |
|---|---|
| Create Docker network | `docker network create flask-network` |
| Run Redis container | `docker run -d --network flask-network redis` |
| Build Flask image | `docker build -t flask-app .` |
| Run Flask container | `docker run -d -p 5000:5000 flask-app` |
| Verify containers | `docker ps` |
| Check container logs | `docker logs <container>` |
| Test Nginx config | `nginx -t` |
| Restart Nginx | `systemctl restart nginx` |

---

# Security Group Configuration

| Type | Port |
|---|---|
| SSH | 22 |
| HTTP | 80 |

Important:

❌ Flask backend port 5000 not publicly exposed

---

# Real DevOps Concepts Learned

| Concept | Description |
|---|---|
| Reverse Proxy | Nginx forwards traffic internally |
| Backend Isolation | Flask hidden behind Nginx |
| Static File Hosting | Nginx serves frontend |
| Docker Networking | Internal container communication |
| Service Discovery | Container names used as DNS |
| API Gateway Pattern | Centralized request routing |

---

# Production-Style Architecture

This architecture is commonly used in:

- Microservices
- Kubernetes
- Cloud-native applications
- API gateway systems

---

# Key DevOps Learnings

- Nginx efficiently serves static content
- Reverse proxies improve security
- Backend services should remain private
- Docker networks enable container communication
- API routing should be centralized
- Production applications separate frontend and backend layers

---

# Interview Questions

| Question | Answer |
|---|---|
| What is reverse proxy? | Server forwarding requests to backend |
| Why use Nginx with Flask? | Security and routing |
| Why use Docker networking? | Container communication |
| Why use container names instead of IPs? | Docker internal DNS |
| What does `proxy_pass` do? | Routes traffic to backend |
| Why hide Flask behind Nginx? | Backend isolation and security |

---

# Future Improvements

- Add HTTPS using Let's Encrypt
- Add Docker Compose
- Add Jenkins CI/CD pipeline
- Add load balancing
- Add Kubernetes deployment
- Add monitoring and logging

---

# Final Result

✅ Dockerized Flask backend deployed successfully  
✅ Redis integration working correctly  
✅ Docker networking configured successfully  
✅ Nginx reverse proxy configured successfully  
✅ Frontend served through Nginx  
✅ API requests routed internally  
✅ Production-style architecture implemented  
✅ Real-world DevOps troubleshooting completed
