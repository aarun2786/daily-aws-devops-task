# Day-9 — Kubernetes Pods Fundamentals

## Project Overview

This project marks the beginning of Kubernetes hands-on practice using Minikube.

The primary goal of this lab was to deeply understand:

- Kubernetes Pods
- Pod lifecycle
- Pod networking
- Pod YAML manifests
- Port forwarding
- Container orchestration basics

Unlike Docker, Kubernetes does not run containers directly.

Kubernetes manages:

```text
Pods
```

which are the smallest deployable units in Kubernetes.

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Kubernetes | Container orchestration |
| Minikube | Local Kubernetes cluster |
| kubectl | Kubernetes CLI |
| Docker | Container runtime |
| Flask | Demo application |
| Ubuntu Linux | Server environment |
| AWS EC2 | Cloud infrastructure |

---

# Kubernetes Architecture Used

```text
EC2 Instance
      │
      ▼
Minikube Cluster
      │
      ▼
Pod
      │
      ▼
Flask Container
```

---

# What is a Pod?

A Pod is:

```text
Smallest deployable unit in Kubernetes
```

Pods act as wrappers around containers.

Kubernetes NEVER runs containers directly.

It runs:

```text
Pods
```

---

# Pod Features

Pods provide:

- Shared networking
- Shared storage
- Shared lifecycle
- Container grouping

---

# Real Pod Architecture

```text
Pod
 ├── Flask Container
 ├── Pod IP
 └── Shared Storage
```

---

# Why Pods Exist

Containers alone cannot easily provide:

- Shared localhost networking
- Shared storage
- Lifecycle grouping

Pods solve these problems.

---

# Project Structure

```text
Day-9/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── flask-pod.yaml
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
    return "Hello from Kubernetes Pod!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

---

# requirements.txt

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

# Minikube Setup

## Start Cluster

```bash
minikube start --driver=docker
```

---

# Verify Cluster

```bash
kubectl get nodes
```

Expected:

```text
minikube   Ready
```

---

# Important Kubernetes Understanding

Minikube creates:

- Kubernetes Cluster
- Control Plane
- Worker Node
- API Server
- Scheduler
- ETCD

inside the same EC2 instance.

---

# Important Docker Configuration

Before building image:

```bash
eval $(minikube docker-env)
```

---

# Why This Is Important

Minikube uses its own internal Docker daemon.

Without this command:

❌ Kubernetes cannot find locally built Docker images.

---

# Build Docker Image

```bash
docker build -t flask-pod:v1 .
```

---

# Verify Image

```bash
docker images
```

---

# Pod YAML

## flask-pod.yaml

```yaml
apiVersion: v1

kind: Pod

metadata:
  name: flask-pod

spec:
  containers:

    - name: flask-container

      image: flask-pod:v1

      imagePullPolicy: Never

      ports:
        - containerPort: 5000
```

---

# YAML Breakdown

| Field | Purpose |
|---|---|
| apiVersion | Kubernetes API version |
| kind | Kubernetes resource type |
| metadata | Pod details |
| spec | Pod configuration |
| containers | Container list |

---

# Important Configuration

```yaml
imagePullPolicy: Never
```

tells Kubernetes:

✅ Use local Minikube image  
❌ Do not pull from Docker Hub

---

# Create Pod

```bash
kubectl apply -f flask-pod.yaml
```

---

# Verify Pod

```bash
kubectl get pods
```

Expected:

```text
flask-pod   Running
```

---

# Describe Pod

```bash
kubectl describe pod flask-pod
```

This shows:

- Pod IP
- Events
- Container info
- Pod lifecycle
- Resource usage

---

# View Pod Logs

```bash
kubectl logs flask-pod
```

---

# Execute Inside Pod

```bash
kubectl exec -it flask-pod -- bash
```

---

# Test Application Inside Pod

```bash
curl localhost:5000
```

Expected:

```text
Hello from Kubernetes Pod!
```

---

# Important Networking Learning

Inside Pod:

```text
localhost = same pod
```

Containers inside same pod share:

- Same IP
- Same localhost
- Same storage

---

# Port Forwarding

## Command

```bash
kubectl port-forward --address 0.0.0.0 pod/flask-pod 5000:5000
```

---

# Purpose

Temporarily expose Pod to browser.

---

# Browser Access

```text
http://<EC2-PUBLIC-IP>:5000
```

---

# Pod Lifecycle Learned

```text
Pending
   ↓
Running
   ↓
Succeeded / Failed
```

---

# Delete Pod

```bash
kubectl delete pod flask-pod
```

---

# Important Learning

Pods are:

```text
Temporary
```

If deleted:

❌ Pod disappears permanently

This is why Deployments exist later.

---

# Problems Faced During the Project

---

# 1. Kubernetes API Server Unreachable

## Error

```text
failed to download openapi

dial tcp:
connect: no route to host
```

---

# Root Cause

Minikube cluster was not running.

API server became unreachable.

---

# Solution

Verified Minikube status:

```bash
minikube status
```

Restarted cluster:

```bash
minikube start --driver=docker
```

---

# Key Learning

`kubectl` communicates with Kubernetes API server.

If API server stops:

❌ All Kubernetes commands fail.

---

# 2. ImagePullBackOff Error

## Error

```text
ImagePullBackOff
```

---

# Root Cause

Docker image was built outside Minikube Docker environment.

Kubernetes could not find local image.

---

# Solution Procedure

## Step 1

Configured Minikube Docker environment:

```bash
eval $(minikube docker-env)
```

---

# Step 2

Rebuilt Docker image:

```bash
docker build -t flask-pod:v1 .
```

---

# Step 3

Verified YAML contained:

```yaml
imagePullPolicy: Never
```

---

# Step 4

Deleted failed pod:

```bash
kubectl delete pod flask-pod
```

---

# Step 5

Recreated pod:

```bash
kubectl apply -f flask-pod.yaml
```

---

# Key Learning

Minikube uses separate internal Docker daemon.

---

# 3. Port Forward Working But Website Not Opening

## Problem

Port forwarding command executed successfully but browser could not access application.

---

# Root Cause

Default `kubectl port-forward` binds only to:

```text
127.0.0.1
```

inside EC2.

External browser traffic could not reach localhost.

---

# Solution

Used:

```bash
kubectl port-forward --address 0.0.0.0 pod/flask-pod 5000:5000
```

---

# Additional Fix

Opened EC2 Security Group port:

```text
5000
```

---

# Key Learning

| Address | Meaning |
|---|---|
| 127.0.0.1 | Localhost only |
| 0.0.0.0 | All network interfaces |

---

# 4. Understanding Pod Networking

## Learning Outcome

Learned that Pods provide:

- Shared localhost
- Shared networking
- Shared IP addresses

All containers inside same Pod can communicate using:

```text
localhost
```

---

# Important Kubernetes Concepts Learned

| Concept | Description |
|---|---|
| Pod | Smallest deployable unit |
| kubectl | Kubernetes CLI |
| Minikube | Local Kubernetes cluster |
| Pod Lifecycle | Pod states |
| Port Forwarding | Temporary pod exposure |
| Pod Networking | Shared localhost and IP |

---

# Important Commands Used

| Purpose | Command |
|---|---|
| Start Minikube | `minikube start` |
| Check nodes | `kubectl get nodes` |
| Create pod | `kubectl apply -f file.yaml` |
| View pods | `kubectl get pods` |
| Describe pod | `kubectl describe pod` |
| View logs | `kubectl logs pod-name` |
| Exec into pod | `kubectl exec -it` |
| Delete pod | `kubectl delete pod` |
| Port forward | `kubectl port-forward` |

---

# Real DevOps Learning

This project introduced:

- Kubernetes architecture
- Pod management
- Container orchestration
- Kubernetes networking
- Kubernetes troubleshooting
- YAML-based infrastructure

---

# Important Interview Questions

| Question | Answer |
|---|---|
| What is a Pod? | Smallest Kubernetes deployment unit |
| Does Kubernetes run containers directly? | No |
| Why did ImagePullBackOff occur? | Image unavailable inside Minikube |
| Why use `eval $(minikube docker-env)`? | Use Minikube Docker daemon |
| Why did port-forward fail externally? | Bound only to localhost |
| What does `--address 0.0.0.0` do? | Allows external access |

---

# Key DevOps Learnings

- Kubernetes manages Pods, not containers directly
- Pods provide shared networking and storage
- Minikube contains local Kubernetes cluster
- API server is central communication component
- Pod networking is different from Docker networking
- Kubernetes uses declarative YAML configurations

---

# Final Result

✅ Kubernetes cluster configured successfully  
✅ Flask application deployed successfully  
✅ Pod created successfully  
✅ Port forwarding configured successfully  
✅ Pod networking understood successfully  
✅ Kubernetes troubleshooting completed successfully  
✅ Real-world Kubernetes concepts learned
