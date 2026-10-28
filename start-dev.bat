@echo off
title PrepPilot Launcher
echo ==========================================
echo   Starting PrepPilot Development Servers
echo ==========================================

cd /d "%~dp0"

echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000...
start "PrepPilot Backend" cmd /k "cd /d "%~dp0backend" && .\venv\Scripts\python -m uvicorn app.main:app --reload --port 8000"

echo [2/2] Starting React Frontend on http://localhost:5173...
start "PrepPilot Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo Servers are launching in separate windows!
echo - Web App: http://localhost:5173
echo - API Docs: http://127.0.0.1:8000/api/v1/docs
echo.
pause
