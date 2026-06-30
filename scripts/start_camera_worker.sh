#!/usr/bin/env bash
set -e

# Wait for Redis
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 1
done
echo "Redis started"

if [ -z "$SENTINEL_CAMERA_ID" ]; then
    echo "ERROR: SENTINEL_CAMERA_ID environment variable is required."
    exit 1
fi

# Start the Camera Worker
echo "Starting camera worker for camera: $SENTINEL_CAMERA_ID"
exec python -m backend.camera_worker.main
