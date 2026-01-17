# Multi-Environment Deployment Platform

A complete DevOps project demonstrating containerization, CI/CD, and infrastructure automation using modern DevOps practices.

## 🚀 Project Overview

This project showcases a full-stack application with automated deployment pipeline, featuring:
- Microservices architecture
- Containerized services with Docker
- Automated CI/CD pipeline
- Infrastructure as Code (IaC)
- Multi-environment configuration

## 🏗️ Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Frontend   │─────▶│   Backend   │─────▶│  Database   │
│   (Nginx)   │      │   (Flask)   │      │ (PostgreSQL)│
└─────────────┘      └─────────────┘      └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │    Redis    │
                     │   (Cache)   │
                     └─────────────┘
```

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS (Tailwind CSS)
- Vanilla JavaScript
- Nginx web server

### Backend
- Python 3.11
- Flask (Web Framework)
- Gunicorn (WSGI Server)
- Flask-CORS

### Database & Cache
- PostgreSQL 15
- Redis 7

### DevOps Tools
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Terraform (IaC)
- Ansible (Configuration Management)

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose V2
- Git
- Ubuntu 20.04+ or similar Linux distribution

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd multi-env-deployment-platform
```

### 2. Build the images
```bash
# Build backend
cd backend
docker build -t backend-api:v1 .

# Build frontend
cd ../frontend
docker build -t frontend-app:v1 .
```

### 3. Start all services
```bash
cd ..
docker compose up -d
```

### 4. Verify services are running
```bash
docker compose ps
```

### 5. Access the application
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:5005
- **API Health**: http://localhost:5005/health
- **API Status**: http://localhost:5005/api/status

## 📁 Project Structure

```
multi-env-deployment-platform/
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container definition
├── frontend/
│   ├── index.html          # Frontend UI
│   ├── nginx.conf          # Nginx configuration
│   └── Dockerfile          # Frontend container definition
├── docker-compose.yml      # Services orchestration
├── init-db.sql            # Database initialization
└── README.md              # Project documentation
```

## 🔌 API Endpoints

### Health & Status
- `GET /health` - Health check endpoint
- `GET /api/status` - Service status with dependencies

### Items Management
- `GET /api/items` - Get all items
- `POST /api/items` - Create new item
  ```json
  {
    "name": "Item Name",
    "description": "Item Description"
  }
  ```

### Cache
- `GET /api/cache/test` - Test Redis cache connection

## 🧪 Testing

### Test Backend API
```bash
# Health check
curl http://localhost:5005/health

# Get items
curl http://localhost:5005/api/items

# Create item
curl -X POST http://localhost:5005/api/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Item","description":"Test Description"}'
```

### Test Cache
```bash
curl http://localhost:5005/api/cache/test
```

## 🔧 Development

### View logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

### Rebuild after changes
```bash
# Rebuild specific service
docker compose up -d --build backend

# Rebuild all services
docker compose up -d --build
```

### Stop services
```bash
docker compose down
```

### Clean up (including volumes)
```bash
docker compose down -v
```

## 🌍 Environment Variables

Backend environment variables (configured in docker-compose.yml):
- `DB_HOST` - PostgreSQL host
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `REDIS_HOST` - Redis host
- `REDIS_PORT` - Redis port

## 📊 Monitoring & Health Checks

All services include health checks:
- **Backend**: HTTP health endpoint
- **PostgreSQL**: pg_isready check
- **Redis**: PING command
- **Frontend**: Nginx health endpoint

## 🔐 Security Features

- Environment variable configuration
- CORS configuration
- Nginx security headers
- Health check endpoints
- Container isolation

## 🚦 Next Steps

- [ ] Add CI/CD pipeline with GitHub Actions
- [ ] Implement Infrastructure as Code with Terraform
- [ ] Add monitoring with Prometheus & Grafana
- [ ] Set up multi-environment configurations (Dev/Staging/Prod)
- [ ] Implement automated testing
- [ ] Add Kubernetes deployment manifests

## 📝 Notes

- Default ports can be changed in `docker-compose.yml`
- Database data persists in Docker volume `postgres_data`
- Frontend uses Tailwind CSS from CDN

## 👤 Author

Nour - DevOps Engineer

## 📄 License

This project is open source and available for educational purposes.
