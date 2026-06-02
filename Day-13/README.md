# Day-13 — Kubernetes ConfigMaps

## Objective

Learn how Kubernetes ConfigMaps help separate application configuration from container images and how they can be consumed inside Pods using:

* Environment Variables (`env`)
* Environment Variables (`envFrom`)
* Volume Mounts
* Deployment Integration
* Service Exposure

---

# What is a ConfigMap?

A ConfigMap is a Kubernetes object used to store non-sensitive configuration data as key-value pairs.

Instead of hardcoding configuration inside Docker images, Kubernetes allows us to store configuration separately and inject it into containers at runtime.

## Problem Without ConfigMaps

Suppose an application contains:

```text
DB_HOST=prod-db
LOG_LEVEL=info
```

If these values change:

1. Modify application
2. Build new image
3. Push image
4. Redeploy application

This is inefficient.

## Solution Using ConfigMaps

```text
Application Image
        +
ConfigMap
```

Same Docker image can be deployed across:

* Development
* QA
* Staging
* Production

by changing only the ConfigMap.

---

# Kubernetes Objects Used

## Deployment

Deployment manages Pods and ensures the desired number of replicas are running.

Responsibilities:

* Create Pods
* Replace failed Pods
* Perform rolling updates
* Scale applications

Example:

```text
Deployment
      │
      ▼
ReplicaSet
      │
      ▼
Pods
```

---

## Service

A Service provides a stable network endpoint for Pods.

Why Service?

Pod IPs are temporary.

```text
Pod Deleted
     ↓
New Pod Created
     ↓
New IP Address
```

Services provide a fixed endpoint.

```text
User
  │
  ▼
Service
  │
  ▼
Pods
```

---

# Lab 1 — ConfigMap Using Environment Variables (env)

## ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap

metadata:
  name: app-config

data:
  NAME: Arun
  AGE: "29"
```

Apply:

```bash
kubectl apply -f configmap.yaml
```

---

## Deployment

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: flask-deployment

spec:
  replicas: 1

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
        image: ubuntu:22.04

        command:
        - tail
        - -f
        - /dev/null

        env:
        - name: USER_NAME
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: NAME

        - name: USER_AGE
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: AGE
```

---

## Understanding env

```yaml
- name: USER_NAME
```

Environment variable inside container.

```yaml
key: NAME
```

Key from ConfigMap.

Result:

```text
NAME (ConfigMap)
      ↓
USER_NAME (Container)
```

Verification:

```bash
kubectl exec -it <pod-name> -- sh

echo $USER_NAME
echo $USER_AGE
```

Output:

```text
Arun
29
```

---

# Lab 2 — ConfigMap Using envFrom

Instead of mapping each variable individually, import all variables.

## ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap

metadata:
  name: app-config

data:
  NAME: Arun
  AGE: "29"
  CITY: Mysore
```

---

## Deployment

```yaml
envFrom:
- configMapRef:
    name: app-config
```

Complete Container Section:

```yaml
containers:
- name: flask-container
  image: ubuntu:22.04

  command:
  - tail
  - -f
  - /dev/null

  envFrom:
  - configMapRef:
      name: app-config
```

---

## Understanding envFrom

Kubernetes automatically imports all keys.

```text
ConfigMap

NAME=Arun
AGE=29
CITY=Mysore
```

Becomes:

```text
NAME=Arun
AGE=29
CITY=Mysore
```

inside container.

Verification:

```bash
kubectl exec -it <pod-name> -- printenv
```

Output:

```text
NAME=Arun
AGE=29
CITY=Mysore
```

---

# Lab 3 — ConfigMap Using Volume Mount

## Theory

When ConfigMap is mounted as a volume:

```text
ConfigMap Key
      ↓
File Name

ConfigMap Value
      ↓
File Content
```

---

## My Example

Created file:

```html
<h1>Hello Arun from ConfigMap</h1>
```

Create ConfigMap:

```bash
kubectl create configmap nginx-html \
--from-file=index.html
```

---

## Deployment

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: nginx-deployment

spec:
  replicas: 1

  selector:
    matchLabels:
      app: nginx

  template:
    metadata:
      labels:
        app: nginx

    spec:
      containers:
      - name: nginx
        image: nginx

        volumeMounts:
        - name: html-volume
          mountPath: /usr/share/nginx/html

      volumes:
      - name: html-volume
        configMap:
          name: nginx-html
```

---

## Verification

```bash
kubectl exec -it <pod-name> -- sh
```

Check file:

```bash
cat /usr/share/nginx/html/index.html
```

Output:

```html
<h1>Hello Arun from ConfigMap</h1>
```

---

# Important Learning

I modified the original `index.html` file on the EC2 instance and expected Kubernetes to update automatically.

It did NOT update.

Reason:

```text
EC2 File
     ↓
ConfigMap Created
     ↓
Stored in etcd
```

Kubernetes stores a snapshot of the file content.

Updating the original file does not update the ConfigMap.

Need to recreate or update the ConfigMap.

Example:

```bash
kubectl create configmap nginx-html \
--from-file=index.html \
-o yaml --dry-run=client | kubectl apply -f -
```

---

# ConfigMap Update Behavior

| Method       | Auto Update |
| ------------ | ----------- |
| env          | No          |
| envFrom      | No          |
| Volume Mount | Yes         |

Volume-mounted ConfigMaps typically refresh within 30-60 seconds.

Environment variables require Pod restart.

```bash
kubectl rollout restart deployment nginx-deployment
```

---

# Interview Questions

## What is a ConfigMap?

A ConfigMap is a Kubernetes object used to store non-sensitive configuration data separately from container images.

---

## Difference Between env and envFrom?

### env

Imports specific keys.

```yaml
env:
```

### envFrom

Imports all keys.

```yaml
envFrom:
```

---

## Does ConfigMap Update Automatically?

Depends on consumption method:

* Environment Variables → No
* Volume Mount → Yes

---

## Why Use ConfigMaps?

* Separate configuration from code
* Reuse same image across environments
* Simplify deployments
* Improve maintainability

---

# Key Takeaways

* Deployment manages Pods.
* Service provides stable networking.
* ConfigMap stores application configuration.
* env imports individual keys.
* envFrom imports all keys.
* Volume Mounts expose ConfigMap data as files.
* Updating the original EC2 file does not update the ConfigMap automatically.
* Volume-mounted ConfigMaps can refresh automatically.
* Environment-variable ConfigMaps require Pod restart.

