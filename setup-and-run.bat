@echo off
setlocal enabledelayedexpansion

echo ============================================
echo Personal Cloud Storage - Auto Setup
echo ============================================
echo.
echo [INFO] Setting up on remote PC...
echo.

REM ============================================
REM 1. CHECK AND INSTALL PYTHON
REM ============================================
echo [STEP 1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Python is not installed!
    echo [INFO] Downloading Python 3.12...
    
    REM Download Python installer
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile '%TEMP%\python-installer.exe'}"
    
    if exist "%TEMP%\python-installer.exe" (
        echo [INFO] Installing Python (this may take a few minutes)...
        "%TEMP%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        
        REM Refresh PATH
        call refreshenv >nul 2>&1
        
        REM Check again
        python --version >nul 2>&1
        if %errorlevel% neq 0 (
            echo [ERROR] Python installation failed. Please install manually from: https://www.python.org/downloads/
            pause
            exit /b 1
        )
        
        del "%TEMP%\python-installer.exe"
        echo [OK] Python installed successfully
    ) else (
        echo [ERROR] Failed to download Python installer
        echo [INFO] Please install Python manually from: https://www.python.org/downloads/
        pause
        exit /b 1
    )
) else (
    echo [OK] Python is installed
    python --version
)
echo.

REM ============================================
REM 2. UPGRADE PIP AND INSTALL DEPENDENCIES
REM ============================================
echo [STEP 2/5] Installing Backend Dependencies...
cd backend
python -m pip install --upgrade pip --quiet
echo [INFO] Installing latest versions of all packages...
python -m pip install Flask Flask-CORS Pillow watchdog requests --upgrade
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] All dependencies installed (latest versions)
echo.

REM ============================================
REM 3. CHECK AND INSTALL NGROK
REM ============================================
echo [STEP 3/5] Checking ngrok installation...
ngrok version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] ngrok is not installed!
    echo [INFO] Downloading ngrok...
    
    REM Download ngrok
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile '%TEMP%\ngrok.zip'}"
    
    if exist "%TEMP%\ngrok.zip" (
        echo [INFO] Extracting ngrok...
        powershell -Command "Expand-Archive -Path '%TEMP%\ngrok.zip' -DestinationPath '%USERPROFILE%\ngrok' -Force"
        
        REM Add to PATH for this session
        set "PATH=%PATH%;%USERPROFILE%\ngrok"
        
        REM Add to system PATH permanently
        powershell -Command "& {[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + ';%USERPROFILE%\ngrok', 'User')}"
        
        del "%TEMP%\ngrok.zip"
        echo [OK] ngrok installed successfully
        echo [INFO] Location: %USERPROFILE%\ngrok\ngrok.exe
    ) else (
        echo [WARNING] Failed to download ngrok
        echo [INFO] You can install it manually from: https://ngrok.com/download
    )
) else (
    echo [OK] ngrok is installed
    ngrok version
)
echo.

REM ============================================
REM 4. CREATE STORAGE DIRECTORY
REM ============================================
echo [STEP 4/5] Setting up storage...
if not exist "C:\Users\%USERNAME%\MyCloud\Photos" (
    mkdir "C:\Users\%USERNAME%\MyCloud\Photos"
    echo [OK] Created storage directory: C:\Users\%USERNAME%\MyCloud\Photos
) else (
    echo [OK] Storage directory exists
)

REM Initialize database
python -c "from database import Database; db = Database(); print('[OK] Database initialized')" 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Database initialization skipped
)
echo.

REM ============================================
REM 5. START BACKEND AND NGROK
REM ============================================
echo [STEP 5/5] Starting services...
echo.
echo ============================================
echo BACKEND SERVER STARTING...
echo ============================================
echo Local: http://localhost:5000
echo.

REM Check if ngrok is available
where ngrok >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Starting ngrok in background...
    start "Ngrok Tunnel" cmd /c "ngrok http 5000"
    timeout /t 3 /nobreak >nul
    echo.
    echo ============================================
    echo NGROK TUNNEL ACTIVE
    echo ============================================
    echo [INFO] Check ngrok URL at: http://localhost:4040
    echo [INFO] Or run: curl http://localhost:4040/api/tunnels
    echo.
    echo Copy the ngrok URL and add it to Vercel:
    echo   Settings -^> Environment Variables -^> REACT_APP_API_URL
    echo.
) else (
    echo [INFO] Ngrok not available - server only on localhost
    echo [INFO] Install ngrok from: https://ngrok.com/download
    echo.
)

echo ============================================
echo BACKEND SERVER RUNNING
echo ============================================
echo [IMPORTANT] Keep this window open!
echo [IMPORTANT] Press Ctrl+C to stop
echo.

python app.py

pause
