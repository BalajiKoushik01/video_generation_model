@echo off
echo ==================================================
echo 🎬 HOLLYWOOD STUDIO - OFFLINE MODE
echo ==================================================
echo.
echo Setting environment variables for Offline use...
set LLM_PROVIDER=ollama
set ENABLE_COMFYUI=True
set VOICEOVER_PROVIDER=edge-tts
echo.

echo 🔍 Checking for Ollama...
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo ⚠️ Ollama not found in PATH! 
    echo    Please install from https://ollama.com
    echo.
) else (
    echo ✅ Ollama detected.
)

echo 🔍 Checking for Python dependencies...
python -c "import edge_tts; import whisper; import reportlab; import moviepy; print('✅ Dependencies found')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️ Dependencies missing. Installing...
    pip install edge-tts websocket-client openai-whisper reportlab moviepy
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies. Audio/Subtitles might not work.
    )
)

echo.
echo 🚀 Starting Studio...
python studio.py
pause
