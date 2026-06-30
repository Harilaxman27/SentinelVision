#!/usr/bin/env bash
set -e

# Wait for Postgres
echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL started"

# Wait for Redis
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 1
done
echo "Redis started"

# Run Alembic migrations
echo "Running database migrations..."
alembic upgrade head

# Start the API server
echo "Starting backend API..."
exec uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
