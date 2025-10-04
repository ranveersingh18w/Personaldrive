@echo off
echo ============================================
echo Personal Cloud Storage - Setup and Run
echo ============================================
echo.

REM Check Python
echo [STEP 1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Python is not installed!
    echo [INFO] Downloading and installing Python 3.12 automatically...
    echo [INFO] This may take 5-10 minutes, please wait...
    echo.
    
    REM Download Python installer using PowerShell
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile '%TEMP%\python-installer.exe'"
    
    if not exist "%TEMP%\python-installer.exe" (
        echo [ERROR] Failed to download Python installer
        echo [INFO] Please download manually from: https://www.python.org/downloads/
        echo.
        pause
        exit /b 1
    )
    
    echo [INFO] Installing Python - this will take a few minutes...
    "%TEMP%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    REM Wait for installation to complete
    echo [INFO] Waiting for installation to complete...
    timeout /t 20 /nobreak >nul
    
    REM Delete installer
    del "%TEMP%\python-installer.exe"
    
    echo [OK] Python installed successfully!
    echo.
    echo [IMPORTANT] Please CLOSE this window and run setup-and-run.bat again
    echo [IMPORTANT] This is needed to refresh the PATH environment variable
    echo.
    pause
    exit /b 0
)

echo [OK] Python is installed
python --version
echo.

REM Install dependencies
echo [STEP 2/5] Installing dependencies...
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
echo [STEP 3/5] Checking ngrok...
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
echo [STEP 4/5] Setting up storage...
if not exist "C:\Users\%USERNAME%\MyCloud\Photos" mkdir "C:\Users\%USERNAME%\MyCloud\Photos"
echo [OK] Storage ready: C:\Users\%USERNAME%\MyCloud\Photos
echo.

REM Initialize database
python -c "from database import Database; db = Database(); print('[OK] Database initialized')" 2>nul

echo [STEP 5/5] Starting Backend Server...
echo ============================================
echo Backend Server Starting...
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
