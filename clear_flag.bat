@echo off
title Clear Processing Flag

echo Clearing stuck flag...
wsl -e bash -c "cd /mnt/c/YOUR_PROJECT_PATH && docker exec n8n_core rm -f /root/.n8n-files/.processing && echo Done"

echo.
echo Flag cleared. n8n will pick up the next file within 1 minute.
echo.
pause
