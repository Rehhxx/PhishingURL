@echo off
title Phishing URL Detection App

REM Change to your project directory
cd /d "%~dp0"

REM Activate virtual environment
call myenv\Scripts\activate

REM Start FastAPI backend in a new window
start "FastAPI Server" cmd /k "uvicorn app:app --reload"

REM Wait for a moment to ensure backend starts before launching frontend
timeout /t 2 >nul

REM Start Streamlit frontend in a new window
start "Streamlit App" cmd /k "streamlit run appUI.py"

REM Optional: Run test script in another window
:: start "Run Test Script" cmd /k "python test_api.py"

echo All services launched. Close this window if not needed.
pause
