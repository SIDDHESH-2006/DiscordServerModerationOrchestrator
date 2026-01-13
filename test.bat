@echo off
REM Quick test for Windows users
REM Run this to quickly verify bot is working

setlocal enabledelayedexpansion

echo.
echo ====================================================
echo  Discord Bot Quick Test
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo [1/3] Checking configuration...
python validate.py
if %errorlevel% neq 0 (
    echo.
    echo Configuration check failed. Fix the issues above.
    pause
    exit /b 1
)

echo.
echo [2/3] Starting backend in 5 seconds...
echo   Open another terminal while this runs!
echo.
timeout /t 5

start /b cmd /c "python main.py --mode backend"

echo.
echo [3/3] Starting bot in 3 seconds...
echo.
timeout /t 3

python main.py --mode bot

echo.
echo Bot has been closed.
pause
