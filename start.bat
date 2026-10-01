@echo off
echo Starting AI Crowd Density & Abnormal Behavior Detection Application
echo.

echo [1/2] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python app.py"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && node node_modules/vite/bin/vite.js"

echo.
echo ==========================================
echo Application is starting...
echo Frontend: http://localhost:3000
echo Backend: http://localhost:5000
echo ==========================================
echo.
echo Press any key to close this window...
pause >nul
