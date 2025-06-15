# ⚡ Usage Billing Tracker System

A scalable, modular usage-based billing backend built with **FastAPI**, **PostgreSQL**, **Celery**, and **Redis** — containerized with **Docker**.

## 📦 Features

- 📊 Submit and retrieve usage events per user
- 🧾 Generate reports via background job processing (Celery)
- 🔄 Job status tracking by job ID
- 🐳 Dockerized with PostgreSQL and Redis for async task queueing
- ✅ API documented with Swagger UI (`/docs`)
- 🔬 Includes unit tests and GitHub Actions CI

---

## 🚀 Quickstart

### 🔧 Requirements

- Docker + Docker Compose
- Python 3.10+ (for local development/testing)

### 🐳 Run with Docker Compose

```bash
docker-compose up --build
