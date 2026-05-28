# Day-10 — Kubernetes Deployments & ReplicaSets

## Project Overview

This project focused on understanding Kubernetes Deployments and ReplicaSets.

Previously, Pods were created manually. However, standalone Pods are temporary and not self-healing.

This lab introduced:

- Deployments
- ReplicaSets
- Self-healing
- Scaling
- Automated Pod management

This is one of the most important Kubernetes concepts used in real-world production environments.

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

# Kubernetes Deployment Architecture

```text
Deployment
    ↓
ReplicaSet
    ↓
Pods
    ↓
Containers
```

---

# Why Deployments Exist

Standalone Pods have limitations:

- No self-healing
- No scaling
- No rolling updates
- Manual management

Deployments solve these problems.

---

# Real Deployment Workflow

```text
Deployment
     ↓
ReplicaSet
     ↓
Multiple Pods
```

---

# Real-World Benefits

Deployments provide:

- Self-healing
- Auto scaling
- Pod management
- Rolling updates
- High availability

---

# Project Structure

```text
Day-10/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── flask-deployment.yaml
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
    return "Hello from Kubernetes Deployment!"

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

# Minikube Docker Environment

Before building the image:

```bash
eval $(minikube docker-env)
```

---

# Why This Is Important

Minikube uses its own internal Docker daemon.

Without this command:

❌ Kubernetes cannot access locally built images.

---

# Build Docker Image

```bash
docker build -t flask-deploy:v1 .
```

---

# Verify Docker Image

```bash
docker images
```

---

# Deployment YAML

## flask-deployment.yaml

```yaml
apiVersion: apps/v1

kind: Deployment

metadata:
  name: flask-deployment

spec:

  replicas: 2

  selector:
    matchLabels:
      app: flask

  template:

    metadata:
      labels:
        app: flask

    spec:

      containers:

        - name: flask-container

          image: flask-deploy:v1

          imagePullPolicy: Never

          ports:
            - containerPort: 5000
```

---

# YAML Breakdown

| Field | Purpose |
|---|---|
| apiVersion | Kubernetes API version |
| kind | Resource type |
| replicas | Number of Pods |
| selector | Finds matching Pods |
| labels | Pod identification |
| template | Pod blueprint |

---

# Important Configuration

```yaml
imagePullPolicy: Never
```

tells Kubernetes:

✅ Use local Minikube image  
❌ Do not pull image from Docker Hub

---

# Create Deployment

```bash
kubectl apply -f flask-deployment.yaml
```

---

# Verify Deployment

```bash
kubectl get deployments
```

Expected:

```text
flask-deployment
```

---

# Verify ReplicaSets

```bash
kubectl get rs
```

---

# Verify Pods

```bash
kubectl get pods
```

Expected:

```text
2 Running Pods
```

---

# Important Observation

Creating:

```text
1 Deployment
```

automatically created:

- ReplicaSet
- Multiple Pods

---

# Describe Deployment

```bash
kubectl describe deployment flask-deployment
```

This displays:

- Replica information
- Pod status
- Deployment events
- Scaling information

---

# Self-Healing Demonstration

## Delete One Pod

```bash
kubectl delete pod <pod-name>
```

---

# Verify Pods Again

```bash
kubectl get pods
```

---

# Important Observation

Kubernetes automatically created a new replacement Pod.

---

# This Feature Is Called

```text
Self-Healing
```

One of Kubernetes' most powerful capabilities.

---

# Scaling Deployment

## Increase Replicas

```bash
kubectl scale deployment flask-deployment --replicas=4
```

---

# Verify Scaling

```bash
kubectl get pods
```

Expected:

```text
4 Running Pods
```

---

# Scale Down

```bash
kubectl scale deployment flask-deployment --replicas=1
```

---

# Port Forward Deployment

```bash
kubectl port-forward --address 0.0.0.0 deployment/flask-deployment 5000:5000
```

---

# Browser Access

```text
http://<EC2-PUBLIC-IP>:5000
```

Expected:

```text
Hello from Kubernetes Deployment!
```

---

# View Deployment YAML from Cluster

```bash
kubectl get deployment flask-deployment -o yaml
```

---

# Delete Deployment

```bash
kubectl delete deployment flask-deployment
```

---

# Important Observation

Deleting Deployment automatically deleted:

- ReplicaSet
- Pods

---

# Problems Faced During the Project

---

# 1. Wrong API Version in Deployment YAML

## Error

```text
no matches for kind "Deployment" in version "app/v1"
```

---

# Root Cause

Incorrect API version used:

```yaml
apiVersion: app/v1
```

Correct version is:

```yaml
apiVersion: apps/v1
```

---

# Solution

Updated YAML configuration:

```yaml
apiVersion: apps/v1
```

---

# Key Learning

Deployments belong to:

```text
apps API group
```

---

# 2. ImagePullBackOff Error

## Error

```text
ImagePullBackOff
```

---

# Root Cause

Docker image was built outside Minikube Docker environment.

---

# Solution

Configured Minikube Docker daemon:

```bash
eval $(minikube docker-env)
```

Rebuilt image:

```bash
docker build -t flask-deploy:v1 .
```

---

# Key Learning

Minikube uses its own internal Docker environment.

---

# 3. Port Forward Working But Website Not Opening

## Problem

Port forwarding succeeded but browser could not access application.

---

# Root Cause

Default `kubectl port-forward` binds only to localhost.

---

# Solution

Used:

```bash
kubectl port-forward --address 0.0.0.0 deployment/flask-deployment 5000:5000
```

Opened EC2 Security Group port:

```text
5000
```

---

# Key Learning

| Address | Meaning |
|---|---|
| 127.0.0.1 | Localhost only |
| 0.0.0.0 | All interfaces |

---

# 4. Understanding ReplicaSets

## Learning Outcome

Learned that ReplicaSets:

- Maintain desired pod count
- Automatically recreate failed Pods
- Work behind Deployments

---

# Important Kubernetes Concepts Learned

| Concept | Description |
|---|---|
| Deployment | Manages Pods |
| ReplicaSet | Maintains replicas |
| Self-Healing | Auto pod recreation |
| Scaling | Multiple pod replicas |
| Rolling Updates | Safe application updates |

---

# Important Commands Used

| Purpose | Command |
|---|---|
| Create deployment | `kubectl apply -f` |
| View deployments | `kubectl get deployments` |
| View ReplicaSets | `kubectl get rs` |
| View Pods | `kubectl get pods` |
| Describe deployment | `kubectl describe deployment` |
| Scale deployment | `kubectl scale deployment` |
| Delete deployment | `kubectl delete deployment` |
| Port forward | `kubectl port-forward` |

---

# Real DevOps Learning

This project introduced:

- Kubernetes self-healing
- Replica management
- Scaling applications
- Automated workload management
- Kubernetes declarative infrastructure

---

# Real Production Benefits

Deployments help production systems achieve:

- High availability
- Fault tolerance
- Zero downtime deployments
- Automatic recovery
- Horizontal scaling

---

# Important Interview Questions

| Question | Answer |
|---|---|
| What is Deployment? | Kubernetes resource managing Pods |
| What is ReplicaSet? | Maintains desired Pod count |
| Why use Deployments instead of Pods? | Self-healing and scaling |
| What happens if Pod crashes? | ReplicaSet recreates Pod |
| What is self-healing? | Automatic pod recovery |
| Why use `apps/v1`? | Correct API group for Deployments |

---

# Key DevOps Learnings

- Deployments manage ReplicaSets
- ReplicaSets manage Pods
- Kubernetes automatically heals failed Pods
- Scaling becomes easy using Deployments
- Kubernetes uses declarative YAML infrastructure
- Deployments are production-ready workloads

---

# Final Result

✅ Kubernetes Deployment created successfully  
✅ ReplicaSet created successfully  
✅ Multiple Pods running successfully  
✅ Self-healing verified successfully  
✅ Scaling verified successfully  
✅ Port forwarding configured successfully  
✅ Kubernetes Deployment architecture understood successfully
