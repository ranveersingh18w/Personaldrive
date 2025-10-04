@echo off
echo ========================================
echo Personal Cloud Storage - Starting All Services
echo ========================================
echo.

echo [1/4] Checking dependencies...
cd backend
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo Installing backend dependencies...
    pip install Flask==2.3.3 Flask-CORS==4.0.0 watchdog==3.0.0 --quiet
    pip install --upgrade Pillow --quiet
    if errorlevel 1 (
        echo WARNING: Pillow installation failed - thumbnails disabled
    )
)
cd ..
echo Dependencies OK!
echo.

echo [2/4] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python app.py"
timeout /t 5 >nul

echo [3/4] Starting Upload Client...
start "Upload Client" cmd /k "cd client && python uploader.py"
timeout /t 2 >nul

echo [4/4] Starting Web Interface...
start "Web Interface" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo All services started!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Three windows should have opened:
echo   1. Backend Server (Flask)
echo   2. Upload Client (Python)
echo   3. Web Interface (React)
echo.
echo Wait ~30 seconds for frontend to compile, then visit:
echo   http://localhost:3000
echo.
echo Close this window to keep services running.
echo.
pause
