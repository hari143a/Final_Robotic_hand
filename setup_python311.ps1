# Setup Python 3.11 for MediaPipe Compatibility
# MediaPipe requires Python 3.8-3.11 (Python 3.13 not supported yet)

Write-Host "=== Python 3.11 Setup for MediaPipe ===" -ForegroundColor Cyan
Write-Host ""

# Check if Python 3.11 is already installed
Write-Host "Checking for Python 3.11..." -ForegroundColor Yellow
$python311 = & py -3.11 --version 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Python 3.11 is installed: $python311" -ForegroundColor Green
    Write-Host ""
    Write-Host "Creating virtual environment with Python 3.11..." -ForegroundColor Yellow
    
    # Create venv with Python 3.11
    py -3.11 -m venv venv311
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Virtual environment created!" -ForegroundColor Green
        Write-Host ""
        Write-Host "To activate and install packages:" -ForegroundColor Cyan
        Write-Host "  .\venv311\Scripts\Activate.ps1" -ForegroundColor White
        Write-Host "  pip install opencv-python mediapipe requests" -ForegroundColor White
    } else {
        Write-Host "[ERROR] Failed to create virtual environment" -ForegroundColor Red
    }
} else {
    Write-Host "[WARNING] Python 3.11 is not installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.11:" -ForegroundColor Yellow
    Write-Host "  1. Download from: https://www.python.org/downloads/release/python-3118/" -ForegroundColor White
    Write-Host "  2. During installation, check 'Add Python to PATH'" -ForegroundColor White
    Write-Host "  3. Run this script again" -ForegroundColor White
    Write-Host ""
    Write-Host "Or install without MediaPipe (if not needed):" -ForegroundColor Yellow
    Write-Host "  pip install opencv-python requests" -ForegroundColor White
}

Write-Host ""
Write-Host "Note: MediaPipe doesn't support Python 3.13 yet." -ForegroundColor Yellow
Write-Host "Current Python version: $(python --version)" -ForegroundColor Yellow

