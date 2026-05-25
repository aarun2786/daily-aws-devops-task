# Docker Compose Multi-Container Project — Flask + Redis

## Project Overview

This project demonstrates how to deploy and manage a multi-container application using:

- Docker Compose
- Flask
- Redis
- Docker Networking
- AWS EC2
- Linux

The application uses Redis as a backend service to store and track visit counts while Flask serves the web application.

This project helps understand:

- Multi-container architecture
- Docker Compose orchestration
- Container networking
- Service dependency management
- Docker troubleshooting

---

# Architecture

```text
                 Docker Compose
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
  Flask Container                 Redis Container
        │                               │
        └──── Internal Docker Network ──┘
```

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| Flask | Python web framework |
| Redis | In-memory database |
| AWS EC2 | Hosting environment |
| Linux | Server administration |

---

# Project Structure

```text
Day-5/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# Flask Application

## app.py

```python
from flask import Flask
import redis

app = Flask(__name__)

redis_client = redis.Redis(host='redis', port=6379)

@app.route('/')
def home():
    redis_client.incr('hits')
    return f"Container Visits: {redis_client.get('hits').decode('utf-8')}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

---

# Requirements File

## requirements.txt

```text
Flask==3.0.0
redis==5.0.1
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

# Docker Compose File

## docker-compose.yml

```yaml
version: '3.8'

services:

  app:
    image: flask-redis:latest

    ports:
      - "5000:5000"

    depends_on:
      - redis

  redis:
    image: redis:latest

    container_name: redis-server
```

---

# Build & Deployment Steps

---

# Step 1 — Build Docker Image

```bash
docker build -t flask-redis .
```

---

# Step 2 — Validate Compose File

```bash
docker compose config
```

---

# Step 3 — Start Multi-Container Environment

```bash
docker compose up -d
```

---

# Step 4 — Verify Running Containers

```bash
docker ps
```

Expected Containers:

```text
flask-app
redis-server
```

---

# Step 5 — Access Application

```text
http://<public-ip>:5000
```

Example Output:

```text
Container Visits: 1
```

Refreshing browser increments Redis counter.

---

# Step 6 — Check Logs

View all logs:

```bash
docker compose logs
```

View Flask logs:

```bash
docker compose logs app
```

---

# Step 7 — Stop Environment

```bash
docker compose down
```

---

# Container Communication Flow

```text
Browser
   ↓
Flask Container
   ↓
Redis Container
   ↓
Store Visit Count
```

---

# Docker Networking Concept

Docker Compose automatically creates:

✅ Internal bridge network

Containers communicate using:

```text
service names
```

Example:

```python
redis.Redis(host='redis', port=6379)
```

Where:

```text
redis
```

is the Docker Compose service name.

---

# Problems Faced & Solutions

---

## 1. Invalid Compose YAML Syntax

### Problem

```text
additional properties 'service' not allowed
```

### Root Cause

Used:

```yaml
service:
```

instead of:

```yaml
services:
```

### Solution

Corrected root Docker Compose keyword.

---

## 2. Volume Mapping Error

### Problem

```text
volumes must be a mapping
```

### Root Cause

Incorrect YAML structure for volumes section.

### Solution

Fixed YAML indentation and structure.

---

## 3. Flask Application File Missing

### Problem

```text
app/app/app.py file not found
```

### Root Cause

Docker volume:

```yaml
volumes:
  - app_vol:/app
```

overrode `/app` directory inside container and hid application files.

### Solution

Removed unnecessary volume mapping.

---

## 4. Container Communication Failure

### Problem

Flask unable to connect to Redis.

### Root Cause

Incorrect Redis hostname.

### Solution

Used Docker Compose service name:

```python
host='redis'
```

---

# Important Docker Compose Commands

| Purpose | Command |
|---|---|
| Validate compose file | `docker compose config` |
| Start containers | `docker compose up -d` |
| Stop containers | `docker compose down` |
| View logs | `docker compose logs` |
| Restart services | `docker compose restart` |
| View running containers | `docker ps` |

---

# Docker Concepts Learned

| Concept | Description |
|---|---|
| Multi-container architecture | Multiple services working together |
| Internal Docker networking | Containers communicate internally |
| Compose orchestration | Manage services together |
| Service dependency | `depends_on` startup control |
| Container isolation | Separate runtime environments |

---

# Real DevOps Learning

This project demonstrates how modern applications are built using:

- Microservices
- Container-based deployments
- Service orchestration
- Infrastructure automation

Real production systems often use:

- Flask/Django APIs
- Redis caching
- PostgreSQL/MySQL
- Nginx reverse proxy
- Kubernetes orchestration

---

# Security Group Configuration

| Type | Port | Source |
|---|---|---|
| SSH | 22 | Your IP |
| Flask App | 5000 | 0.0.0.0/0 |

---

# Important Debugging Commands

| Purpose | Command |
|---|---|
| Check container logs | `docker logs <container>` |
| Validate YAML | `docker compose config` |
| Check running services | `docker ps` |
| Remove containers | `docker compose down` |
| Remove unused volumes | `docker volume prune` |

---

# Key DevOps Takeaways

## Docker Compose Simplifies Multi-Container Management

Instead of manually starting containers one by one, Docker Compose manages:

- Networking
- Startup order
- Service dependencies
- Environment orchestration

---

## Service Discovery

Containers communicate using service names instead of IP addresses.

---

## YAML Accuracy Is Critical

Docker Compose is highly dependent on:

- Proper indentation
- Correct structure
- Accurate service definitions

---

# Interview Questions

| Question | Answer |
|---|---|
| Why use Docker Compose? | Manage multi-container applications |
| How do containers communicate in Compose? | Internal Docker network |
| What does `depends_on` do? | Controls service startup order |
| Why did `app.py` disappear? | Volume mapping overrode container filesystem |
| Why use Redis with Flask? | Caching and state management |
| What command validates Compose syntax? | `docker compose config` |

---

# Future Improvements

- Add Nginx reverse proxy
- Add PostgreSQL database
- Use Docker volumes properly
- Add Jenkins CI/CD pipeline
- Deploy on Kubernetes
- Add environment variables
- Add health checks

---

# Final Result

✅ Multi-container environment deployed successfully  
✅ Flask container connected to Redis successfully  
✅ Docker Compose orchestration completed  
✅ Container networking verified  
✅ Redis visit counter working correctly  
✅ Real-world Docker troubleshooting completed
