@echo off
echo 🎬 Hollywood Studio Launcher 🎬
echo --------------------------------
echo Using Python Environment: c:\Users\balaj\Desktop\AI\.venv\Scripts\python.exe

"c:\Users\balaj\Desktop\AI\.venv\Scripts\python.exe" "c:\Users\balaj\Desktop\AI\Hollywood_Studio\gui.py"

if %errorlevel% neq 0 (
    echo.
    echo ❌ The application crashed or failed to start.
    echo Installing dependencies to be safe...
    "c:\Users\balaj\Desktop\AI\.venv\Scripts\python.exe" -m pip install customtkinter requests websocket-client "moviepy<2.0" python-dotenv huggingface_hub
    echo.
    echo Retrying launch...
    "c:\Users\balaj\Desktop\AI\.venv\Scripts\python.exe" "c:\Users\balaj\Desktop\AI\Hollywood_Studio\gui.py"
)

pause
