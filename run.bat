@echo off
REM Discord Server Moderation Orchestrator - Startup Script

echo.
echo =========================================================
echo  Discord Server Moderation Orchestrator
echo =========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

REM Install dependencies
echo [1/4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Dependencies installed successfully!
echo.
echo [3/4] Starting Discord Bot & Backend...
echo.
echo =========================================================
echo  IMPORTANT: Open TWO separate terminals
echo =========================================================
echo.
echo Terminal 1 (Backend API):
echo   python main.py --mode backend
echo.
echo Terminal 2 (Discord Bot):
echo   python main.py --mode bot
echo.
echo Or run this script again and select your option.
echo.

choice /C 123 /M "Select: (1) Start Backend (2) Start Bot (3) Both guides"

if errorlevel 3 goto :both
if errorlevel 2 goto :bot
if errorlevel 1 goto :backend

:backend
echo [4/4] Starting FastAPI Backend...
echo.
python main.py --mode backend
goto :end

:bot
echo [4/4] Starting Discord Bot...
echo.
python main.py --mode bot
goto :end

:both
echo.
echo To run BOTH, you need TWO SEPARATE terminals:
echo.
echo Option A - Using VS Code Terminal:
echo   - Ctrl+Shift+` (open integrated terminal)
echo   - Run: python main.py --mode backend
echo   - Ctrl+Shift+` again (open second terminal)
echo   - Run: python main.py --mode bot
echo.
echo Option B - Using Command Prompt:
echo   - First window: python main.py --mode backend
echo   - Second window: python main.py --mode bot
echo.
pause

:end
pause
