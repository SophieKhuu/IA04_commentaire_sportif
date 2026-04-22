@echo off
REM Installation script for Volleyball Commentary Analyzer on Windows

echo ============================================================
echo  Volleyball Commentary Analyzer - Installation Script
echo ============================================================
echo.

REM Check if .venv exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
) else (
    echo Virtual environment already exists
)

echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt

echo.
echo Creating .env file from example...
if not exist ".env" (
    copy .env.example .env
    echo Please edit .env and add your GROQ_API_KEY
) else (
    echo .env already exists
)

echo.
echo ============================================================
echo Installation complete!
echo.
echo Next steps:
echo  1. Edit .env and add your GROQ_API_KEY
echo  2. Run: streamlit run main.py
echo ============================================================
pause
