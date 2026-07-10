# AI Ecosystem Workspace

Docker Compose environment สำหรับ AI/Data Labeling workflow

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| Redis | `redis:8.8.0-alpine` | 6379 | In-memory data store |
| PostgreSQL | `postgres:17` | 5432 | Relational database |
| Label Studio | `heartexlabs/label-studio:latest` | 8080 | Data labeling platform |

## Quick Start

```bash
# Copy and configure environment
cp .env.sample .env
# Edit .env with your credentials

# Start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

## Access

- **Label Studio**: http://localhost:8080
- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`

## Volumes

| Volume | Purpose |
|--------|--------|
| `redis-data` | Redis persistence |
| `postgresql-data` | PostgreSQL data |
| `label-studio-data` | Label Studio projects & data |

## Repository

https://github.com/KIM2548TH/ai-ecosystem-workspace