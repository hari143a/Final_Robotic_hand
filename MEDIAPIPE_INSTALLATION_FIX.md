# MediaPipe Installation Fix for Python 3.13

## Problem
```
ERROR: Could not find a version that satisfies the requirement mediapipe (from versions: none)
```

## Root Cause
**MediaPipe doesn't support Python 3.13.2 yet.** MediaPipe currently supports Python **3.8 to 3.11** only.

Your current Python version: **Python 3.13.2** ❌

## Solutions

### Option 1: Use Python 3.11 (Recommended)

1. **Install Python 3.11:**
   - Download from: https://www.python.org/downloads/release/python-3118/
   - During installation, check "Add Python to PATH"
   - Or use pyenv-win: `pyenv install 3.11.8`

2. **Create a virtual environment with Python 3.11:**
   ```powershell
   # Check available Python versions
   py -3.11 --version
   
   # Create virtual environment with Python 3.11
   py -3.11 -m venv venv
   
   # Activate it
   .\venv\Scripts\Activate.ps1
   
   # Now install packages
   pip install opencv-python mediapipe requests
   ```

### Option 2: Use pyenv-win (Manage Multiple Python Versions)

1. **Install pyenv-win:**
   ```powershell
   # Using PowerShell (run as Administrator)
   Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"
   & "./install-pyenv-win.ps1"
   ```

2. **Install Python 3.11:**
   ```powershell
   pyenv install 3.11.8
   pyenv global 3.11.8
   ```

3. **Verify and install packages:**
   ```powershell
   python --version  # Should show 3.11.8
   pip install opencv-python mediapipe requests
   ```

### Option 3: Use Conda/Miniconda (Alternative)

1. **Install Miniconda:** https://docs.conda.io/en/latest/miniconda.html

2. **Create environment with Python 3.11:**
   ```powershell
   conda create -n esp32 python=3.11
   conda activate esp32
   pip install opencv-python mediapipe requests
   ```

### Option 4: Install Without MediaPipe (If Not Needed)

If you don't actually need MediaPipe, just install the others:

```powershell
pip install opencv-python requests
```

### Option 5: Wait for MediaPipe Python 3.13 Support

Check MediaPipe releases: https://github.com/google/mediapipe/releases
- MediaPipe typically adds support for new Python versions a few months after release
- Python 3.13 was released in October 2024, support may come in 2025

## Quick Check: What Python Version Do You Need?

Check MediaPipe requirements:
```powershell
pip show mediapipe
```

Or check PyPI page: https://pypi.org/project/mediapipe/

## Verification

After installing Python 3.11 and activating the environment:

```powershell
python --version  # Should show 3.11.x
pip install opencv-python mediapipe requests
pip list  # Verify all packages installed
```

## Note About ESP32 Projects

**Important:** If you're developing for ESP32 (MicroPython), these packages (`opencv-python`, `mediapipe`) are **desktop Python packages** and won't run on ESP32.

ESP32 MicroPython doesn't support:
- opencv-python
- mediapipe
- Most standard Python libraries

If you need computer vision on ESP32, consider:
- Using ESP32-CAM with basic image processing
- Sending images to a desktop/server for processing
- Using edge AI models specifically built for ESP32

## Recommended Setup for ESP32 + Desktop Processing

```
Desktop Computer (Python 3.11):
├── opencv-python  # Image processing
├── mediapipe      # Pose/hand tracking
├── requests       # HTTP communication
└── Flask/FastAPI  # API server

ESP32 (MicroPython):
├── machine.Pin    # GPIO control
├── network       # WiFi connectivity
├── urequests     # HTTP requests (lite version)
└── ujson         # JSON handling
```

The ESP32 can send data/images to the desktop for processing, or receive commands from the desktop.

