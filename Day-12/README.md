# Day-12 — Kubernetes Labels, Selectors & Namespaces

## Project Overview

This project focused on understanding how Kubernetes organizes and isolates resources using Labels, Selectors, and Namespaces.

In real-world environments, a single Kubernetes cluster may host applications for multiple environments such as Development, Testing, and Production. Namespaces help isolate these environments while Labels and Selectors help Kubernetes identify and manage resources.

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

## Labels

Labels are key-value pairs attached to Kubernetes objects.

Example:

```yaml
labels:
  app: flask
  env: dev
```

Labels help identify, group, and filter resources.

---

## Selectors

Selectors use labels to find matching resources.

Example:

```yaml
selector:
  app: flask
```

This tells Kubernetes:

```text
Find all Pods where app=flask
```

Services use selectors to discover Pods and route traffic.

---

## Namespaces

Namespaces logically separate resources within the same Kubernetes cluster.

Example:

```text
Cluster
│
├── default
├── dev
├── test
└── prod
```

Namespaces allow multiple teams or environments to share a cluster safely.

---

# Real-World Scenario

A company maintains separate environments for:

```text
Development
Testing
Production
```

Instead of creating separate clusters, all environments are hosted in a single Kubernetes cluster using namespaces.

---

# Namespace Creation

Created namespaces:

```bash
kubectl create namespace dev
kubectl create namespace test
kubectl create namespace prod
```

Verified:

```bash
kubectl get ns

NAME              STATUS   AGE
backend           Active   2m54s
default           Active   2d1h
dev               Active   60m
frontend          Active   2m54s
kube-node-lease   Active   2d1h
kube-public       Active   2d1h
kube-system       Active   2d1h
prod              Active   58m
test              Active   58m
```

---

# Deployments in Multiple Environments

Created the same Flask Deployment in multiple namespaces.

## Development Namespace

```bash
kubectl get deployment -n dev --show-labels
```

Output:

```text
NAME               READY   UP-TO-DATE   AVAILABLE   AGE   LABELS
flask-deployment   2/2     2            2           62m   env=dev,type=deploy
```

## Test Namespace

```bash
kubectl get deployment -n test --show-labels 
```

Output:

```text
NAME               READY   UP-TO-DATE   AVAILABLE   AGE   LABELS
flask-deployment   2/2     2            2           59m   env=test,type=deploy
```

## Production Namespace

```bash
kubectl get deployment -n prod --show-labels 
```

Output:

```text
NAME               READY   UP-TO-DATE   AVAILABLE   AGE   LABELS
flask-deployment   2/2     2            2           51m   env=prod,type=deploy
```

---

# Pod Verification

Verified Pods across all namespaces:

```bash
kubectl get pods -A
```

Output:

```text
NAMESPACE     NAME                                       READY   STATUS    RESTARTS       AGE
default       flask-deployment-65fcdf68d-g82gs           1/1     Running   0              60m
default       flask-deployment-65fcdf68d-jmpx4           1/1     Running   0              60m
dev           flask-deployment-dccc5fb84-847ww           1/1     Running   0              65m
dev           flask-deployment-dccc5fb84-g98pr           1/1     Running   0              65m
kube-system   calico-kube-controllers-59556d9b4c-xrkbp   1/1     Running   1 (142m ago)   2d1h
kube-system   calico-node-8nkqj                          1/1     Running   1 (142m ago)   2d1h
kube-system   coredns-66bc5c9577-2jfx2                   1/1     Running   1 (142m ago)   2d1h
kube-system   coredns-66bc5c9577-m2xrg                   1/1     Running   1 (142m ago)   2d1h
kube-system   etcd-ip-172-31-31-169                      1/1     Running   1 (142m ago)   2d1h
kube-system   kube-apiserver-ip-172-31-31-169            1/1     Running   1 (142m ago)   2d1h
kube-system   kube-controller-manager-ip-172-31-31-169   1/1     Running   1 (142m ago)   2d1h
kube-system   kube-proxy-z6q2h                           1/1     Running   1 (142m ago)   2d1h
kube-system   kube-scheduler-ip-172-31-31-169            1/1     Running   1 (142m ago)   2d1h
prod          flask-deployment-65fcdf68d-g2nb8           1/1     Running   0              53m
prod          flask-deployment-65fcdf68d-prqhc           1/1     Running   0              53m
test          flask-deployment-58c6bf6989-75h2q          1/1     Running   0              61m
test          flask-deployment-58c6bf6989-vx5kj          1/1     Running   0              61m
```

This confirmed that identical application deployments can exist in different namespaces.

---

# Service Creation

Created NodePort Service in the Development namespace.

Verified:

```bash
kubectl get service -A
```

Output:

```text
NAMESPACE     NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                  AGE
default       kubernetes      ClusterIP   10.96.0.1       <none>        443/TCP                  2d1h
dev           flask-service   NodePort    10.96.253.163   <none>        5000:32660/TCP           31m
kube-system   kube-dns        ClusterIP   10.96.0.10      <none>        53/UDP,53/TCP,9153/TCP   2d1h

```

---

# Namespace Isolation Test

Checked resources in each namespace:

```bash
kubectl get pods -n dev

kubectl get pods -n test

kubectl get pods -n prod
```

Verified that resources remained isolated inside their respective namespaces.

Even though all deployments had the same name:

```text
flask-deployment
```

they coexisted because they belonged to different namespaces.

---

# Switching Namespace Context

Check current namespace:

```bash
kubectl config view --minify | grep namespace
```

Switch namespace:

```bash
kubectl config set-context --current --namespace=dev
```

Switch to test:

```bash
kubectl config set-context --current --namespace=test
```

Switch to production:

```bash
kubectl config set-context --current --namespace=prod
```

Return to default:

```bash
kubectl config set-context --current --namespace=default
```

---

# Actual Cluster Resources

## Pods

```text
default : 2 Pods
dev     : 2 Pods
test    : 2 Pods
prod    : 2 Pods
```

## Deployments

```text
default : flask-deployment
dev     : flask-deployment
test    : flask-deployment
prod    : flask-deployment
```

## Services

```text
dev : flask-service (NodePort)
```

---

# Problems Faced During the Project

## 1. Resources Not Visible

### Problem

Running:

```bash
kubectl get pods
```

did not display Pods from dev, test, or prod namespaces.

### Root Cause

kubectl only shows resources from the current namespace.

### Resolution

Specified namespace explicitly:

```bash
kubectl get pods -n dev

kubectl get pods -n test

kubectl get pods -n prod
```

### Learning

Resources are isolated by namespace.

---

## 2. Confusion About Deployments with Same Name

### Problem

The same deployment name existed in multiple environments:

```text
flask-deployment
```

### Observation

Deployments successfully coexisted in:

```text
default
dev
test
prod
```

### Learning

Namespaces provide logical isolation, allowing resources with identical names to exist in different environments.

---

# Key Learnings

* Labels help identify Kubernetes resources.
* Selectors find resources using labels.
* Services use selectors to discover Pods.
* Namespaces isolate environments.
* Multiple deployments with the same name can exist in different namespaces.
* Namespaces are widely used to separate Development, Testing, and Production workloads.
* Kubernetes clusters can host multiple environments safely.

---

# Interview Questions

### What are Labels?

Labels are key-value metadata attached to Kubernetes resources for identification and grouping.

### What are Selectors?

Selectors use labels to locate Kubernetes resources.

### What are Namespaces?

Namespaces logically separate resources inside a Kubernetes cluster.

### Can two namespaces contain deployments with the same name?

Yes. Namespaces provide isolation, allowing resources with the same name to exist in different namespaces.

### Why do companies use namespaces?

To separate environments such as Development, Testing, and Production while using the same Kubernetes cluster.

---

# Final Result

✅ Labels Understood

✅ Selectors Understood

✅ dev Namespace Created

✅ test Namespace Created

✅ prod Namespace Created

✅ Namespace Isolation Verified

✅ Same Deployment Deployed Across Multiple Environments

✅ Day-12 Completed Successfully

