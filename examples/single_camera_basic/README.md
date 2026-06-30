# Example: Single Camera (Basic)

Minimal configuration for one camera with the shoplifting plugin.

## Running

`ash
cp examples/single_camera_basic/sentinel.yaml config/sentinel.yaml
docker compose -f docker/docker-compose.yml up -d
python backend/main.py
`\n