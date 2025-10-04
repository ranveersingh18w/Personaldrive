@echo off
echo ============================================
echo Personal Cloud Storage - Setup and Run
echo ============================================
echo.

REM Check Python
echo [STEP 1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please download and install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)
echo [OK] Python is installed
python --version
echo.

REM Install dependencies
echo [STEP 2/4] Installing dependencies...
cd backend
python -m pip install --upgrade pip --quiet
python -m pip install Flask Flask-CORS Pillow watchdog requests --upgrade
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] All dependencies installed
echo.

REM Check ngrok
echo [STEP 3/4] Checking ngrok...
where ngrok >nul 2>&1
if errorlevel 1 (
    echo [WARNING] ngrok is not installed
    echo.
    echo To access from anywhere, install ngrok:
    echo 1. Download from: https://ngrok.com/download
    echo 2. Extract ngrok.exe to a folder
    echo 3. Add that folder to your PATH
    echo.
    echo [INFO] Server will run on localhost only
    echo.
) else (
    echo [OK] ngrok is installed
    ngrok version
)
echo.

REM Create storage
echo [STEP 4/4] Setting up storage...
if not exist "C:\Users\%USERNAME%\MyCloud\Photos" mkdir "C:\Users\%USERNAME%\MyCloud\Photos"
echo [OK] Storage ready: C:\Users\%USERNAME%\MyCloud\Photos
echo.

REM Initialize database
python -c "from database import Database; db = Database(); print('[OK] Database initialized')" 2>nul

echo ============================================
echo Starting Backend Server...
echo ============================================
echo.
echo Local access: http://localhost:5000
echo.

REM Try to start ngrok if available
where ngrok >nul 2>&1
if not errorlevel 1 (
    echo [INFO] Starting ngrok tunnel...
    start "Ngrok Tunnel" cmd /c "ngrok http 5000"
    timeout /t 2 /nobreak >nul
    echo [OK] Ngrok started! Check URL at: http://localhost:4040
    echo.
)

echo [IMPORTANT] Keep this window open!
echo [IMPORTANT] Press Ctrl+C to stop the server
echo.
echo ============================================
echo.

python app.py

pause
