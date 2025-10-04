@echo off
echo ========================================
echo Personal Cloud Storage - Full Setup
echo ========================================
echo.
echo This script will set up all components:
echo 1. Backend Server
echo 2. Upload Client
echo 3. Web Interface
echo.
echo Press any key to start installation...
pause >nul

echo.
echo [1/3] Setting up Backend...
cd backend
pip install -r requirements.txt
cd ..

echo.
echo [2/3] Setting up Client...
cd client
pip install -r requirements.txt
cd ..

echo.
echo [3/3] Setting up Frontend...
cd frontend
call npm install
cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the services:
echo   1. Run start-backend.bat
echo   2. Run start-client.bat (optional)
echo   3. Run start-frontend.bat
echo.
echo Or start them all at once with:
echo   start-all.bat
echo.
pause
