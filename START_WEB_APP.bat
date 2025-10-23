@echo off
REM MediaCrawler Web Dashboard Startup Script
REM This script starts the web application on Windows

echo ============================================================
echo   MediaCrawler Web Dashboard
echo ============================================================
echo.
echo Starting web server...
echo.

REM Change to MediaCrawler directory
cd /d "%~dp0"

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the web application
python webapp\app.py

pause

