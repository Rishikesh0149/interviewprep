# PrepPilot Development Launcher
# Starts FastAPI backend (port 8000) and Vite frontend (port 5173) in separate windows

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Starting PrepPilot Development Servers  " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$backendPath = Join-Path $PSScriptRoot "backend"
$frontendPath = Join-Path $PSScriptRoot "frontend"

# Launch Backend
Write-Host "[1/2] Launching Backend on http://127.0.0.1:8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; .\venv\Scripts\python -m uvicorn app.main:app --reload --port 8000"

# Launch Frontend
Write-Host "[2/2] Launching Frontend on http://localhost:5173..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm run dev"

Write-Host "`nReady! Access PrepPilot at: http://localhost:5173" -ForegroundColor Yellow
Write-Host "API documentation at: http://127.0.0.1:8000/api/v1/docs`n" -ForegroundColor Yellow
