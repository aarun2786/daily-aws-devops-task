# Docker Volumes + Persistent Redis Data

## Project Overview

This project demonstrates how to use Docker Volumes for persistent Redis data storage.

The goal of this project was to understand:

- Docker volumes
- Persistent storage
- Stateful containers
- Redis persistence
- Data recovery after container deletion
- Docker storage architecture

Unlike stateless containers, Redis stores important runtime data that must survive container restarts or deletions.

---

# Architecture

```text
Flask Container
      │
      ▼
Redis Container
      │
      ▼
Docker Volume
(Persistent Storage)
```

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Docker | Containerization |
| Redis | In-memory database |
| Docker Volume | Persistent storage |
| Ubuntu Linux | Server environment |
| AWS EC2 | Cloud infrastructure |

---

# Why Docker Volumes?

By default:

```text
Delete container = delete data
```

Docker volumes separate:

- Container lifecycle
- Persistent storage

This allows data to survive:

- Container restarts
- Container deletion
- Image rebuilds

---

# Redis Persistence Setup

---

# Step 1 — Create Docker Volume

```bash
docker volume create redis-data
```

---

# Verify Volume

```bash
docker volume ls
```

Expected:

```text
redis-data
```

---

# Step 2 — Create Docker Network

```bash
docker network create flask-network
```

---

# Step 3 — Run Redis Container with Volume

```bash
docker run -d \
--name redis-server \
--network flask-network \
-v redis-data:/data \
redis redis-server --appendonly yes
```

---

# Important Breakdown

## Volume Mount

```bash
-v redis-data:/data
```

| Part | Meaning |
|---|---|
| redis-data | Docker managed volume |
| /data | Redis internal storage directory |

---

# Redis Persistence

## Append Only File (AOF)

```bash
redis-server --appendonly yes
```

enables Redis persistence on disk.

Without this:

❌ Data stored only in memory

With this:

✅ Data written to persistent storage

---

# Step 4 — Verify Running Container

```bash
docker ps
```

---

# Step 5 — Test Redis Persistence

Connect to Redis container:

```bash
docker exec -it redis-server redis-cli
```

---

# Store Data

```bash
SET user_count 10
```

---

# Verify Data

```bash
GET user_count
```

Expected:

```text
"10"
```

---

# Step 6 — Remove Container

```bash
docker stop redis-server

docker rm redis-server
```

---

# Step 7 — Recreate Redis Container

```bash
docker run -d \
--name redis-server \
--network flask-network \
-v redis-data:/data \
redis redis-server --appendonly yes
```

---

# Step 8 — Verify Persistent Data

Connect again:

```bash
docker exec -it redis-server redis-cli
```

Run:

```bash
GET user_count
```

Expected:

```text
"10"
```

Data survived container deletion.

---

# Docker Volume Location

Docker stores volumes at:

```text
/var/lib/docker/volumes/
```

Specific volume path:

```text
/var/lib/docker/volumes/redis-data/_data
```

---

# Inspect Docker Volume

```bash
docker volume inspect redis-data
```

---

# Verify Redis Files

```bash
sudo ls /var/lib/docker/volumes/redis-data/_data
```

Expected:

```text
appendonly.aof
dump.rdb
```

---

# Problems Faced During the Project

---

# 1. Redis Data Disappeared After Container Deletion

## Problem

After deleting Redis container:

```bash
docker rm redis-server
```

all Redis data was lost.

---

# Root Cause

Redis data was stored only inside container filesystem.

Container storage is temporary.

---

# Solution

Created persistent Docker volume:

```bash
docker volume create redis-data
```

Mounted volume:

```bash
-v redis-data:/data
```

---

# 2. Redis Persistence Not Working

## Problem

Data still disappeared even after using Docker volume.

---

# Root Cause

Redis persistence mode was not enabled.

Redis stored data only in memory.

---

# Solution

Started Redis using:

```bash
redis redis-server --appendonly yes
```

This enabled AOF persistence.

---

# 3. Container-to-Container Communication Issue

## Error

```text
Temporary failure in name resolution
```

---

# Root Cause

Flask and Redis containers were not connected to same Docker network.

---

# Solution

Created shared Docker network:

```bash
docker network create flask-network
```

Connected both containers using:

```bash
--network flask-network
```

Used Redis container name:

```python
host='redis-server'
```

instead of:

```python
host='localhost'
```

---

# 4. Redis Port Already in Use

## Error

```text
address already in use
```

---

# Root Cause

Another Redis process/container was already using port:

```text
6379
```

---

# Solution

Checked active process:

```bash
sudo ss -tulnp | grep 6379
```

Stopped conflicting service/container before restarting Redis.

---

# 5. Understanding Docker Storage Architecture

## Learning Outcome

Learned the difference between:

| Storage Type | Behavior |
|---|---|
| Container filesystem | Temporary |
| Docker Volume | Persistent |

---

# Important Docker Concepts Learned

| Concept | Description |
|---|---|
| Persistent Storage | Data survives container deletion |
| Stateful Containers | Containers storing important data |
| Docker Volumes | External persistent storage |
| Bind Mounts | Host directory mapping |
| Redis Persistence | Saving memory data to disk |

---

# Difference Between Stateless & Stateful Containers

| Stateless | Stateful |
|---|---|
| Flask | Redis |
| Nginx | MySQL |
| Frontend | PostgreSQL |

Stateful services require persistent storage.

---

# Real DevOps Architecture

```text
Application Container
        │
        ▼
Persistent Storage
        │
        ▼
Cloud Block Storage
(AWS EBS)
```

---

# AWS Infrastructure Connection

| Docker | AWS Equivalent |
|---|---|
| Docker Volume | EBS Volume |
| Persistent Storage | Block Storage |
| Mounted Volume | Attached EBS |

---

# Important Commands Used

| Purpose | Command |
|---|---|
| Create volume | `docker volume create redis-data` |
| List volumes | `docker volume ls` |
| Inspect volume | `docker volume inspect redis-data` |
| Create network | `docker network create flask-network` |
| View networks | `docker network ls` |
| Verify Redis data | `redis-cli GET user_count` |

---

# Key DevOps Learnings

- Containers are temporary by default
- Volumes provide persistent storage
- Redis requires persistence configuration
- Docker networks enable internal communication
- Stateful services require durable storage
- Data should survive container lifecycle changes

---

# Interview Questions

| Question | Answer |
|---|---|
| Why use Docker volumes? | Persistent container storage |
| Why did Redis data disappear? | Container filesystem is temporary |
| What does `-v redis-data:/data` do? | Mounts persistent storage |
| Why use `--appendonly yes`? | Enables Redis disk persistence |
| Difference between bind mount and volume? | Host-managed vs Docker-managed storage |
| Why same Docker network needed? | Container communication & DNS resolution |

---

# Future Improvements

- Use Docker Compose
- Add Redis replication
- Add Redis backup automation
- Add monitoring with Prometheus
- Store Redis data on AWS EBS
- Add Kubernetes persistent volumes

---

# Final Result

✅ Docker volume created successfully  
✅ Redis persistence configured successfully  
✅ Data survived container deletion  
✅ Container networking configured successfully  
✅ Persistent storage architecture implemented  
✅ Real-world Docker storage concepts learned
