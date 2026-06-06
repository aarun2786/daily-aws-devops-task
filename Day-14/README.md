# Day-14 — Kubernetes Persistent Volumes (PV) & Persistent Volume Claims (PVC)

## Project Overview

This project focused on understanding Kubernetes persistent storage using Persistent Volumes (PV) and Persistent Volume Claims (PVC).

Containers and Pods are temporary in nature. When a Pod is deleted, all data stored inside the container filesystem is lost. Persistent storage solves this problem by storing data outside the Pod lifecycle.

---

# Technologies Used

* Kubernetes
* kubeadm Cluster
* kubectl
* Docker
* Flask
* Ubuntu Linux
* AWS EC2

---

# What is a Persistent Volume (PV)?

A Persistent Volume (PV) is a storage resource available inside a Kubernetes cluster.

Examples:

* AWS EBS Volume
* NFS Storage
* Azure Disk
* Local Disk

Example:

```text
Persistent Volume
      ↓
1Gi Storage
```

---

# What is a Persistent Volume Claim (PVC)?

A PVC is a request for storage made by an application.

Example:

```text
Application
     ↓
PVC Request
     ↓
Persistent Volume
```

PVC allows developers to request storage without worrying about the underlying storage implementation.

---

# Why Do We Need PV and PVC?

Without PVC:

```text
Pod Deleted
     ↓
Data Lost ❌
```

With PVC:

```text
Pod Deleted
     ↓
New Pod Created
     ↓
Data Still Exists ✅
```

---

# Architecture

```text
Application Pod
      ↓
Persistent Volume Claim (PVC)
      ↓
Persistent Volume (PV)
      ↓
Physical Storage
```

---

# Step 1 — Create Persistent Volume

Created:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: host-based-pv
  labels:
    PV: host-pv
spec:
  capacity:
    storage: 1Gi

  accessModes:
   - ReadWriteOnce

  hostPath:
   path: /home/devops/Day-14/PV
```

Applied:

```bash
kubectl apply -f pv.yaml
```

Verified:

```bash
kubectl get pv

```
Output:

```bash
NAME            CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                    STORAGECLASS   VOLUMEATTRIBUTESCLASS  REASON   AGE
host-based-pv   1Gi        RWO            Retain           Bound    default/pvc-host-based                  <unset>                          105m
```

---

# Step 2 — Create Persistent Volume Claim

Created:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-host-based

spec:
  resources:
    requests:
      storage: 500Mi

  selector:
    matchLabels:
      PV: host-pv

  accessModes:
   - ReadWriteOnce
```

Applied:

```bash
kubectl apply -f pvc.yaml
```

Verified:

```bash
kubectl get pvc
```

Output:

```text
NAME             STATUS   VOLUME          CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
pvc-host-based   Bound    host-based-pv   1Gi        RWO                           <unset>                 87m
```

---

# Step 3 — Mount PVC to Deployment

Attached PVC to the application deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pv-deploy
  labels:
    app: deploy

spec:
  replicas: 3

  selector:
    matchLabels:
      app: flask


  template:
    metadata:
      name: pvc-pod
      labels:
        app: flask


    spec:
      containers:
        - name: pvc-flask-containers
          image: aarun2786/flask-img:v4
          imagePullPolicy: IfNotPresent
          ports:
          - containerPort: 5000

          volumeMounts:
          - name: pvc-host
            mountPath: /app/data


      volumes:
       - name: pvc-host
         persistentVolumeClaim:
          claimName: pvc-host-based

```

---

# Step 4 — Verify Persistent Storage

Entered Pod:

```bash
kubectl exec -it pv-deploy-5c8cbc55bd-26hh7 -- /bin/bash
```

Created file:

```bash
cat << 'EOF' > pvc.py
import socket
import os

# Get the hostname of the pod
hostname = socket.gethostname()

# Get the current working directory (the Python equivalent of pwd)
current_dir = os.getcwd()

# Store them in your dictionary
data = {
    "Directory": current_dir,
    "HostName": hostname
}

print(data)
EOF
```

Verified:

```bash
python3 /app/data/pvc.txt
```

Output:

```text
{'Curent_Folder': '/app/data', 'Host Name': 'pv-deploy-5c8cbc55bd-26hh7'}
```

---

# Step 5 — Verify Data Persistence

Deleted Pod:

```bash
kubectl delete pod <pod-name>
```

Kubernetes automatically created a replacement Pod.

Entered new Pod:

```bash
kubectl exec -it <new-pod> -- sh
```

Verified:

```bash
cat /app/data/test.txt
```

Output:

```text
Hello PVC
```

Data persisted successfully.

---

# Important Commands Used

```bash
kubectl get pv

kubectl get pvc

kubectl describe pvc nginx-pvc

kubectl get pods

kubectl describe pod <pod-name>

kubectl exec -it <pod-name> -- sh
```

---

# Problems Faced During the Project

## Problem 1 — Unknown Field "spec.selector.PV"

### Error

```text
strict decoding error:
unknown field "spec.selector.PV"
```

### Root Cause

Attempted to bind PVC to a PV using:

```yaml
selector:
  PV: nginx-pv
```

This is not a valid PVC field.

### Resolution

Removed the invalid selector and allowed Kubernetes to bind automatically.

Alternatively:

```yaml
selector:
  matchLabels:
    storage: local
```

can be used with PV labels.

### Learning

PVC selectors work with labels, not PV names.

---

## Problem 2 — Application Failed After PVC Mount

### Error

```text
python: can't open file '/app/app.py':
[Errno 2] No such file or directory
```

### Root Cause

The Persistent Volume was mounted directly on:

```text
/app
```

The mount replaced the existing contents of the directory.

As a result:

```text
/app/app.py
```

became inaccessible.

### Resolution

Mounted the PVC to a separate directory:

```text
/app/data
```

instead of:

```text
/app
```

### Learning

Volume mounts replace the contents of the target directory. Never mount a PVC directly on application code directories unless intended.

---

# Key Learnings

* Pods are ephemeral.
* Persistent Volumes provide durable storage.
* PVCs request storage from available PVs.
* PV and PVC must bind successfully.
* Storage survives Pod recreation.
* Volume mounts should not overwrite application directories.
* PVC selectors use labels, not PV names.
* Correct YAML syntax is critical in Kubernetes.

---

# Interview Questions

### What is a Persistent Volume?

A Persistent Volume is a storage resource available in a Kubernetes cluster.

### What is a PVC?

A Persistent Volume Claim is a request for storage made by an application.

### What happens when a Pod using PVC is deleted?

The Pod is deleted, but the data remains on the Persistent Volume.

### Difference Between PV and PVC?

| PV               | PVC                  |
| ---------------- | -------------------- |
| Actual Storage   | Storage Request      |
| Created by Admin | Created by Developer |

### Why did the application fail after mounting a PVC?

Because the PVC was mounted on the application directory, which hid the existing application files.

---

# Final Result

✅ Persistent Volume Created

✅ Persistent Volume Claim Created

✅ PV and PVC Bound Successfully

✅ PVC Mounted to Application

✅ Data Persistence Verified

✅ Pod Recreation Tested

✅ Common PVC Troubleshooting Scenarios Understood

✅ Day-15 Completed Successfully

