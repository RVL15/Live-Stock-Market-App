@echo off
REM Batch helper to create venv, install dependencies, and run the app
where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
  echo 'python' not found. Please install Python 3.8+ and add it to PATH.
  exit /b 1
)

if not exist .venv (
  echo Creating virtual environment .venv...
  python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Upgrading pip and installing requirements...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo Launching app (logs -> run.log)...
python stock_app.py > run.log 2>&1
echo App exited; see run.log for output.
