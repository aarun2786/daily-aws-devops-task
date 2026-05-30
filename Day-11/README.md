# Day-11 — Kubernetes Services (ClusterIP, NodePort & Load Balancing)

## Project Overview

This project focused on understanding Kubernetes Services and how they provide stable networking for Pods.

Previously, applications were accessed directly through Pod IPs. However, Pod IPs are temporary and change whenever Pods are recreated.

Kubernetes Services solve this problem by providing:

* Stable IP addresses
* Stable DNS names
* Service discovery
* Internal load balancing
* External access mechanisms

---

# Technologies Used

* Kubernetes
* kubeadm Cluster
* kubectl
* Docker
* Flask
* AWS EC2
* Ubuntu Linux

---

# Concepts Covered

## ClusterIP

Default Kubernetes Service type.

Used for:

* Internal communication
* Service discovery
* Pod-to-Pod communication

Example:

```text
flask-service.default.svc.cluster.local
```

---

## NodePort

Exposes an application outside the cluster.

Example:

```text
Node IP Range: 30000 - 32767
```

Traffic Flow:

```text
Client
   ↓
NodePort
   ↓
Service
   ↓
Pods
```

---

## LoadBalancer

Used in cloud environments.

Traffic Flow:

```text
Internet
   ↓
Load Balancer
   ↓
Service
   ↓
Pods
```

---

# Deployment

Created a Flask Deployment with multiple replicas.

```bash
kubectl get deployment

NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
flask-deployment                3/3     1            3           38m
flask-deployment-loadbalacing   3/3     3            3           5s

```

Verified Pods:

```bash
kubectl get pods

flask-deployment-594b46484b-j72k4                1/1     Running            0          37m
flask-deployment-594b46484b-ntvqt                1/1     Running            0          37m
flask-deployment-594b46484b-znvjp                1/1     Running            0          37m
flask-deployment-loadbalacing-5458d8dc85-bq9sz   1/1     Running            0          25m
flask-deployment-loadbalacing-5458d8dc85-tnmzq   1/1     Running            0          25m
flask-deployment-loadbalacing-5458d8dc85-x2xp5   1/1     Running            0          25m



```

---

# ClusterIP Service

Created:

```yaml
apiVersion: v1
kind: Service

metadata:
  name: flask-service

spec:
  selector:
    app: flask

  ports:
    - port: 5000
      targetPort: 5000

  type: ClusterIP
```

Applied:

```bash
kubectl apply -f flask-service.yaml
```

---

# Service Discovery Test

Created temporary client pod:

```bash
kubectl run test-pod --image=busybox -it --rm -- sh
```

Tested:

```bash
wget -qO- http://flask-service:5000
```

Successfully accessed application using Service DNS instead of Pod IP.

---

# NodePort Service

Created:

```yaml
apiVersion: v1
kind: Service

metadata:
  name: flask-service

spec:
  selector:
    app: flask

  ports:
    - port: 5000
      targetPort: 5000
      nodePort: 31865

  type: NodePort
```

Applied:

```bash
kubectl apply -f flask-service.yaml
```

Verified:

```bash
kubectl get svc
```

Output:

```text
NAME                          TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
flask-service                 NodePort       10.101.217.5     <none>        5000:32333/TCP   25m
flask-service-loadbalancing   LoadBalancer   10.111.194.230   <pending>     5000:31220/TCP   5m57s
kubernetes                    ClusterIP      10.96.0.1        <none>        443/TCP          121m

```

---

# Endpoint Verification

Verified Service endpoints:

```bash
kubectl get endpoints
```

Output:

```text
NAME                          ENDPOINTS                                                  AGE
flask-service                 192.168.0.158:5000,192.168.0.159:5000,192.168.0.160:5000   45m
flask-service-loadbalancing   192.168.0.158:5000,192.168.0.159:5000,192.168.0.160:5000   25m
kubernetes                    172.31.31.169:6443                                         141m

```

This confirmed that the Service correctly discovered all Pods.

---

# Load Balancing Test

Modified Flask application to return Pod hostname.

Example response:

```text
Served by Pod: flask-deployment-xxxxx
```

Verified Service load balancing by repeatedly accessing the Service with inside ec2 though script .

for i in 1 2 3 4 5 6 7 8 9 10
do
curl http://18.60.142.216:31220
echo
done

devops@ip-172-31-31-169:~/Day-11$ ./script.sh 

Served by Pod: flask-deployment-loadbalacing-5458d8dc85-bq9sz

Served by Pod: flask-deployment-loadbalacing-5458d8dc85-bq9sz

Served by Pod: flask-deployment-loadbalacing-5458d8dc85-bq9sz

Served by Pod: flask-deployment-loadbalacing-5458d8dc85-tnmzq

Served by Pod: flask-deployment-loadbalacing-5458d8dc85-tnmzq

Served by Pod: flask-deployment-loadbalacing-5458d8dc85-bq9sz

Served by Pod: flask-deployment-loadbalacing-5458d8dc85-tnmzq

Served by Pod: flask-deployment-loadbalacing-5458d8dc85-tnmzq

Served by Pod: flask-deployment-loadbalacing-5458d8dc85-x2xp5

Served by Pod: flask-deployment-loadbalacing-5458d8dc85-tnmzq

---

# Important Commands Used

```bash
kubectl get svc

kubectl describe svc flask-service

kubectl get endpoints

kubectl get pods

kubectl describe pod <pod-name>

kubectl run test-pod --image=busybox -it --rm -- sh
```

---

# Problems Faced During the Project

---

## 1. ImagePullBackOff

### Error

```text
ImagePullBackOff
```

### Root Cause

Kubernetes attempted to pull:

```text
docker.io/library/flask-img:v1
```

from Docker Hub but the repository did not exist.

### Resolution

Either:

* Push image to Docker Hub
* Update the yaml file 

```yaml
imagePullPolicy: Always
```

### Learning

Kubernetes pulls images from registries unless configured to use local images.

---

## 2. Security Group Blocking NodePort

### Problem

Website stopped working after removing NodePort rule from EC2 Security Group.

### Root Cause

NodePort traffic was blocked before reaching Kubernetes.

### Resolution

Opened NodePort:

```text
31865
```

in EC2 Security Group.

### Learning

NodePort Services require the NodePort to be allowed through the Security Group.

---

## 3. LoadBalancer Service Showing Pending

### Problem

```text
EXTERNAL-IP: <pending>
```

### Root Cause

The cluster was not integrated with a cloud load balancer provider.

### Resolution

Used the automatically created NodePort instead.

### Learning

LoadBalancer Services require cloud provider integration such as AWS ELB, ALB, or MetalLB.

---

## Key Learnings

* Pod IPs are temporary.
* Services provide stable networking.
* ClusterIP enables internal communication.
* NodePort enables external access.
* Services use labels and selectors to discover Pods.
* Endpoints show backend Pods attached to a Service.
* Kubernetes Services perform load balancing across Pods.
* LoadBalancer Services require cloud provider support.
* Security Groups must allow NodePort traffic.

---

# Final Result

✅ ClusterIP Service Created

✅ NodePort Service Created

✅ Service Discovery Verified

✅ Endpoints Verified

✅ Load Balancing Verified

✅ Kubernetes Networking Concepts Understood

✅ Day-11 Completed Successfully
