@echo off
echo ========================================
echo  Hollywood Studio - ComfyUI Setup
echo  Installing Best-of-Best AI Tools
echo ========================================
echo.

set COMFY_DIR=%~dp0ComfyUI
set VENV_PYTHON=c:\Users\balaj\Desktop\AI\.venv\Scripts\python.exe

echo [1/6] Installing ComfyUI Python Dependencies...
cd "%COMFY_DIR%"
"%VENV_PYTHON%" -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
"%VENV_PYTHON%" -m pip install -r requirements.txt
echo    ✓ Core dependencies installed

echo.
echo [2/6] Installing Custom Nodes Manager...
cd custom_nodes
if not exist "ComfyUI-Manager" (
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git
    echo    ✓ ComfyUI Manager installed
) else (
    echo    ✓ ComfyUI Manager already exists
)

echo.
echo [3/6] Installing HunyuanVideo Node...
if not exist "ComfyUI-HunyuanVideoWrapper" (
    git clone https://github.com/kijai/ComfyUI-HunyuanVideoWrapper.git
    cd ComfyUI-HunyuanVideoWrapper
    "%VENV_PYTHON%" -m pip install -r requirements.txt
    cd ..
    echo    ✓ HunyuanVideo node installed
) else (
    echo    ✓ HunyuanVideo node already exists
)

echo.
echo [4/6] Installing Flux Advanced Nodes...
if not exist "ComfyUI_FluxTrainer" (
    git clone https://github.com/kijai/ComfyUI_FluxTrainer.git
    echo    ✓ Flux Advanced nodes installed
) else (
    echo    ✓ Flux nodes already exist
)

echo.
echo [5/6] Installing Video Processing Nodes...
if not exist "ComfyUI-VideoHelperSuite" (
    git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git
    cd ComfyUI-VideoHelperSuite
    "%VENV_PYTHON%" -m pip install -r requirements.txt
    cd ..
    echo    ✓ Video Helper Suite installed
) else (
    echo    ✓ Video Helper Suite already exists
)

echo.
echo [6/6] Installing RIFE Frame Interpolation...
if not exist "ComfyUI-Frame-Interpolation" (
    git clone https://github.com/Fannovel16/ComfyUI-Frame-Interpolation.git
    cd ComfyUI-Frame-Interpolation
    "%VENV_PYTHON%" -m pip install -r requirements.txt
    cd ..
    echo    ✓ RIFE installed (for 60fps)
) else (
    echo    ✓ RIFE already exists
)

cd ..\..

echo.
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Run: cd ComfyUI
echo 2. Run: python main.py
echo 3. Open browser to: http://127.0.0.1:8188
echo 4. Then run Hollywood Studio GUI
echo.
pause
