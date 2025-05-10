# HeatCode Backend Setup & Deployment Guide

This guide explains how to set up, build Docker images, run services, and handle database migrations for the **HeatCode Backend**.

---

## Clone the Repository

```bash
git clone https://github.com/Naman-0206/code-judge-backend
cd code-judge-backend/setup
```

---

## ▶ Running the Backend Locally

### On **Windows** (PowerShell):

```powershell
.\run_backend_dev.bat
```

### On **Linux**:

```bash
./run_backend_dev.sh
```

---

## Building & Pushing Docker Images

> Run these commands from the `setup/` directory.

### Build, Tag, and Push `server` (Backend API):

```bash
docker build -t heatcode_backend ../server
docker tag heatcode_backend naman0206/heatcode_backend:latest
docker push naman0206/heatcode_backend:latest
```

---

### Build, Tag, and Push `submission-worker`:

```bash
docker build -t submission-worker ../workers/submission_worker
docker tag submission-worker naman0206/submission-worker:latest
docker push submission-worker naman0206/submission-worker:latest
```

---

### Build, Tag, and Push `execution-worker`:

```bash
docker build -t execution-worker ../workers/execution_worker
docker tag execution-worker naman0206/execution-worker:latest
docker push execution-worker naman0206/execution-worker:latest
```

---

## ▶ Running Workers via Docker

Make sure the `.env` file is correctly configured with necessary environment variables.

### Run `submission-worker`:

```bash
docker run -d --name submission-worker --env-file .env naman0206/submission-worker:latest
```

### Run `execution-worker`:

```bash
docker run -d --name execution-worker --env-file .env naman0206/execution-worker:latest
```

---

## 🛠️ Database Migrations with Alembic

### 1. Test on **development** database first.

Make sure `sqlalchemy.url` in `alembic.ini` points to your **dev database**.

### 2. Run upgrades:

```bash
alembic upgrade head
```

### 3. Create new migration:

```bash
alembic revision --autogenerate -m "your message here"
alembic upgrade head
```

This will generate a new migration script in the `alembic/versions/` folder.

---

### Note on Production

Once tested:

- Replace the `sqlalchemy.url` in `alembic.ini` with the **production DB URL**.
- If the production DB is out of sync, run:

```bash
alembic upgrade head
```

---

### Manual Migrations (Optional):

To create a manual migration script without autogeneration:

```bash
alembic revision -m "first migrations"
```
