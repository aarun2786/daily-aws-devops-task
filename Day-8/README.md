# Day-8 — Dockerized Nginx Reverse Proxy with Flask & Redis

## Project Overview

This project demonstrates a fully containerized multi-service architecture using:

- Nginx Reverse Proxy
- Flask Backend API
- Redis Database
- Docker Networking
- Docker Volumes

Unlike previous setups where Nginx was installed directly on the EC2 host, this project containerized the entire application stack.

This helped in understanding:

- Multi-container communication
- Docker networking
- Reverse proxy architecture
- Bind mounts
- Internal DNS resolution
- Production-style container deployments

---

# Architecture

```text
                 Browser
                     │
                     ▼
              Nginx Container
                 Port 80
                     │
             Reverse Proxy
                     │
                     ▼
             Flask Container
                 Port 5000
                     │
                     ▼
              Redis Container
                     │
                     ▼
               Docker Volume
```

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Docker | Containerization |
| Nginx | Reverse Proxy |
| Flask | Backend API |
| Redis | In-memory database |
| Docker Networks | Internal communication |
| Docker Volumes | Persistent storage |
| Ubuntu Linux | Server environment |
| AWS EC2 | Cloud infrastructure |

---

# Project Structure

```text
Day-8/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── index.html
│
└── nginx/
    └── default.conf
```

---

# Why Containerize Nginx?

Previously:

```text
Nginx → Installed directly on EC2
```

Now:

```text
Nginx → Docker Container
```

Benefits:

- Fully portable architecture
- Easier deployment
- Consistent environments
- Infrastructure isolation
- Microservice-style architecture

---

# Docker Network Setup

## Create Network

```bash
docker network create flask-network
```

This network allows:

- Nginx container
- Flask container
- Redis container

to communicate internally using container names.

---

# Redis Container

## Run Redis with Persistent Volume

```bash
docker run -d \
--name redis-server \
--network flask-network \
-v redis-data:/data \
redis redis-server --appendonly yes
```

---

# Flask Backend

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

# Build Flask Image

```bash
docker build -t flask-app .
```

---

# Run Flask Container

```bash
docker run -d \
--name flask-server \
--network flask-network \
flask-app
```

Important:

❌ Port 5000 not publicly exposed

because Nginx handles public traffic.

---

# Frontend HTML

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

# Nginx Reverse Proxy Configuration

## nginx/default.conf

```nginx
server {

    listen 80;

    server_name _;

    root /usr/share/nginx/html/;

    index index.html;

    location / {

        try_files $uri /index.html;
    }

    location /api/ {

        proxy_pass http://flask-server:5000;

        proxy_set_header Host $host;

        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

# Important Reverse Proxy Concept

Nginx container communicates with Flask container using:

```nginx
proxy_pass http://flask-server:5000;
```

because Docker networks provide:

- Internal DNS
- Container name resolution
- Service discovery

---

# Run Nginx Container

```bash
docker run -d \
--name nginx-proxy \
--network flask-network \
-p 80:80 \
-v $(pwd)/nginx/default.conf:/etc/nginx/conf.d/default.conf \
-v $(pwd)/index.html:/usr/share/nginx/html/index.html \
nginx
```

---

# Understanding Bind Mounts

| Host File | Container File |
|---|---|
| `default.conf` | Nginx configuration |
| `index.html` | Frontend page |

---

# Request Flow

```text
Browser
   ↓
Nginx Container
   ↓
Flask Container
   ↓
Redis Container
```

---

# Problems Faced During the Project

---

# 1. Nginx Config Changes Did Not Update Automatically

## Problem

Modified:

```text
default.conf
```

but running Nginx container continued using old configuration.

---

# Root Cause

Bind mount updated the file successfully, but Nginx process had already loaded old config into memory.

---

# Solution

Reloaded Nginx process manually:

```bash
docker exec nginx-proxy nginx -s reload
```

---

# Key Learning

Bind mount updates files on disk, but services must reload configurations into memory.

---

# 2. Wrong Reverse Proxy Backend Target

## Problem

Initially used:

```nginx
proxy_pass http://127.0.0.2:5000;
```

---

# Root Cause

`127.x.x.x` inside container refers only to the same container.

Containers communicate through Docker networks, not localhost.

---

# Solution

Used Flask container name:

```nginx
proxy_pass http://flask-server:5000;
```

---

# Key Learning

Docker networks provide internal DNS resolution using container names.

---

# 3. Missing Frontend Route Handling

## Problem

Frontend HTML did not load correctly.

---

# Root Cause

Nginx lacked:

```nginx
location /
```

configuration.

---

# Solution

Added:

```nginx
location / {

    try_files $uri /index.html;
}
```

---

# 4. Python Virtual Environment Permission Error

## Error

```text
Permission denied
```

while installing Python packages.

---

# Root Cause

Old virtual environment contained root-owned files caused by incorrect `sudo pip install`.

---

# Solution

Removed corrupted environment:

```bash
sudo rm -rf ~/myenv
```

Recreated clean virtual environment.

---

# Key Learning

Never use:

```bash
sudo pip install
```

inside Python virtual environments.

---

# 5. Container Communication Understanding

## Learning Outcome

Learned that:

```text
localhost = same container only
```

Container-to-container communication requires:

- Shared Docker network
- Container names
- Internal Docker DNS

---

# Important Docker Concepts Learned

| Concept | Description |
|---|---|
| Bind Mount | Host file mapped into container |
| Reverse Proxy | Nginx forwarding requests |
| Container DNS | Container name resolution |
| Docker Network | Internal container communication |
| Multi-container Architecture | Multiple services working together |

---

# Important Commands Used

| Purpose | Command |
|---|---|
| Create network | `docker network create flask-network` |
| View containers | `docker ps` |
| Inspect network | `docker network inspect flask-network` |
| Reload Nginx | `docker exec nginx-proxy nginx -s reload` |
| Check Nginx config | `docker exec nginx-proxy nginx -t` |
| View logs | `docker logs <container>` |

---

# Security Benefits Learned

| Benefit | Description |
|---|---|
| Backend Isolation | Flask not publicly exposed |
| Internal Networking | Redis accessible only internally |
| Reverse Proxy Routing | Single public entry point |
| Reduced Attack Surface | Only Nginx exposed publicly |

---

# Real Production Architecture

This setup resembles architectures used in:

- Kubernetes
- Docker Compose
- ECS
- Microservices
- Cloud-native deployments

---

# Key DevOps Learnings

- Containers communicate using Docker networks
- Container names act as hostnames
- Nginx acts as reverse proxy gateway
- Bind mounts provide live file mapping
- Running services cache configs in memory
- Backend services should remain internal/private

---

# Interview Questions

| Question | Answer |
|---|---|
| Why containerize Nginx? | Portable and isolated architecture |
| Why use container names instead of localhost? | Docker internal DNS |
| Why reload Nginx after config changes? | Config loaded into memory |
| What does bind mount do? | Maps host file into container |
| Why no public Flask port? | Backend isolation and security |

---

# Future Improvements

- Use Docker Compose
- Add HTTPS with Let's Encrypt
- Add Nginx load balancing
- Add multiple Flask replicas
- Add Jenkins CI/CD pipeline
- Deploy using Kubernetes

---

# Final Result

✅ Fully containerized architecture deployed successfully  
✅ Nginx reverse proxy container configured successfully  
✅ Flask backend container working correctly  
✅ Redis persistent storage configured successfully  
✅ Internal Docker networking working successfully  
✅ Bind mounts configured correctly  
✅ Production-style architecture implemented  
✅ Real-world DevOps troubleshooting completed
