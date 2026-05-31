<#
PowerShell helper to create venv, install requirements, and run the app.
Usage (PowerShell):
  .\run_app.ps1

Note: if script execution is blocked, run PowerShell as Admin and set:
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
#>
Write-Host "Checking for Python..."
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "'python' not found. Please install Python 3.8+ and ensure 'python' is on PATH." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path -Path .venv)) {
    Write-Host "Creating virtual environment .venv..."
    python -m venv .venv
}

Write-Host "Activating virtual environment..."
. .\.venv\Scripts\Activate.ps1

Write-Host "Upgrading pip and installing requirements..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host "Launching app (logs -> run.log)..."
python stock_app.py *> run.log
Write-Host "App exited; see run.log for output." -ForegroundColor Green
