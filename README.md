# HeatCode Backend Setup & Deployment Guide

Backend service for **HeatCode** — an online code execution & judging platform.  
This repository contains the API server, background workers, and database migration setup.

> ⚠ **Current Status**: This repository is a work in progress. The currently deployed version runs **without workers** — only the API server is active.  
> You can still fully test the system by following this guide to run it locally with workers enabled.

---

## 📦 Tech Stack
- **FastAPI** – REST API framework
- **Docker** – Containerization
- **PostgreSQL** – Database
- **Alembic** – Database migrations
- **RabbitMQ + Workers** – Task processing (submission & execution)

---

## 📥 Clone the Repository
```bash
git clone https://github.com/Naman-0206/code-judge-backend
cd code-judge-backend/setup
````

---

## ▶ Running the Backend Locally

### On **Windows** (PowerShell)

```powershell
.\run_backend_dev.bat
```

### On **Linux**

```bash
./run_backend_dev.sh
```

---

## 🛠 Building & Pushing Docker Images

> Run all commands from the `setup/` directory.
> ⚠ Make sure you are logged in to Docker Hub before pushing.

### 1. Backend API (`server`)

```bash
docker build -t heatcode_backend ../server
docker tag heatcode_backend naman0206/heatcode_backend:latest
docker push naman0206/heatcode_backend:latest
```

### 2. Submission Worker

```bash
docker build -t submission-worker ../workers/submission_worker
docker tag submission-worker naman0206/submission-worker:latest
docker push naman0206/submission-worker:latest
```

### 3. Execution Worker

```bash
docker build -t execution-worker ../workers/execution_worker
docker tag execution-worker naman0206/execution-worker:latest
docker push naman0206/execution-worker:latest
```

---

## ▶ Running Workers via Docker

> Workers are currently **not deployed in production**.

Make sure the `.env` file is correctly configured.

```bash
docker run -d --name submission-worker --env-file .env naman0206/submission-worker:latest
docker run -d --name execution-worker --env-file .env naman0206/execution-worker:latest
```

---

## 🗄 Database Migrations (Alembic)

### 1. Test on Development Database

Ensure `sqlalchemy.url` in `alembic.ini` points to the **dev database**.

### 2. Upgrade

```bash
alembic upgrade head
```

### 3. Create a Migration

```bash
alembic revision --autogenerate -m "your message here"
alembic upgrade head
```

---

### Deploying to Production

* Change `sqlalchemy.url` in `alembic.ini` to production DB URL.
* If DB is out of sync:

```bash
alembic upgrade head
```

---

### Manual Migrations

```bash
alembic revision -m "first migration"
```
