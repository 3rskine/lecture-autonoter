#!/bin/bash
echo ""
echo "========================================"
echo "  Course Automation System - Starting"
echo "========================================"
echo ""

echo "[1/3] Starting Docker containers..."
cd /mnt/c/YOUR_PROJECT_PATH && docker compose up -d
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to start containers."
    echo "Check Docker Desktop WSL Integration settings."
    read -p "Press Enter to exit..."
    exit 1
fi

echo ""
echo "[2/3] Waiting for n8n to be ready..."
count=0
while true; do
    sleep 5
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5678/healthz 2>/dev/null)
    if [ "$STATUS" = "200" ]; then
        echo "  n8n is ready!"
        break
    fi
    count=$((count + 1))
    echo "  Still waiting... ($count/12)"
    if [ $count -ge 12 ]; then
        echo "  WARNING: n8n not responding after 60s, continuing anyway..."
        break
    fi
done

echo ""
echo "[3/3] Container status:"
docker ps --format 'table {{.Names}}\t{{.Status}}'

echo ""
echo "========================================"
echo "  Done! Open http://localhost:5678"
echo "========================================"
echo ""
echo "To clear stuck flag:"
echo "  docker exec n8n_core rm -f /root/.n8n-files/.processing"
echo ""
read -p "Press Enter to exit..."
