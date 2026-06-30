# SentinelVision

> Production-grade Retail Intelligence Platform

## Quick Start

```bash
# 1. Install dependencies
./scripts/setup/setup_dev.sh

# 2. Download AI models
python scripts/models/download_models.py

# 3. Start services
docker compose -f docker/docker-compose.yml up -d

# 4. Run migrations
alembic upgrade head

# 5. Start the application
python backend/main.py
```

## Documentation

- [Architecture](docs/architecture/SentinelVision_Architecture.md)
- [Repository Blueprint](docs/architecture/SentinelVision_Repository_Blueprint.md)
- [Getting Started](docs/guides/getting_started.md)
- [Adding a Plugin](docs/guides/adding_a_plugin.md)
- [Deploying to Production](docs/guides/deploying_production.md)

## Development

```bash
make lint      # Run ruff + mypy
make test      # Run unit tests
make dev       # Start development environment
```
