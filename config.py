"""
Configuration for Hollywood Studio - Enhanced with Multiple AI API Support
"""
import os

# ========== PATHS ==========
OUTPUT_DIR = "C:\\Users\\balaj\\Desktop\\AI\\Hollywood_Studio\\output"
ASSETS_DIR = "C:\\Users\\balaj\\Desktop\\AI\\Hollywood_Studio\\assets"
WORKFLOWS_DIR = "C:\\Users\\balaj\\Desktop\\AI\\Hollywood_Studio\\workflows"

# ========== VIDEO SETTINGS ==========
RESOLUTION = (1920, 1080)  # 1080p
FPS = 24
TARGET_DURATION = 30  # seconds

# ========== AI API KEYS ==========
# Primary: Groq (Fast, Free tier available)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Premium: Anthropic Claude (Best quality for creative work)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Alternative: OpenAI GPT-4 (Industry standard)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# FREE Alternative: HuggingFace Inference API
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")  # Free tier available

# FREE Alternative: Together AI (Free tier)
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")  # Free credits on signup

# Alternative: Google Gemini (Good for vision tasks)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ========== LLM MODEL SELECTION ==========
# ========== LLM MODEL SELECTION ==========
# Provider: "ollama" (Free/Local), "groq" (Fast/Free Tier), "anthropic" (Quality), "openai"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama") 

# Primary models (will try in order)
LLM_MODELS = {
    "super_director": {
        "primary": ("ollama", "llama3"),
        "fallback": [
             ("groq", "llama-3.3-70b-versatile")
        ]
    }
}

# Legacy single model (for backwards compatibility)
LLM_MODEL = "llama3" # Default for Ollama

# ========== OLLAMA SETTINGS (Local/Offline) ==========
# Ensure you have installed Ollama from ollama.com and ran `ollama serve`
OLLAMA_BASE_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# ========== STOCK FOOTAGE APIS ==========
# Pexels (Primary - Best quality, most reliable)
# Get free API key: https://www.pexels.com/api/
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

# Pixabay (Backup)
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "")

# Unsplash (Images only, no key needed for basic use)
# UNSPLASH_API_KEY = "" # Optional

# Freesound (Sound effects)
# Get free API key: https://freesound.org/apiv2/apply/
FREESOUND_API_KEY = os.getenv("FREESOUND_API_KEY", "")

# ========== COMFYUI SETTINGS ==========
COMFYUI_HOST = "127.0.0.1"
COMFYUI_PORT = 8188
VIDEO_MODEL = "hunyuan"  # "hunyuan" or "ltx2"

# ========== VOICEOVER SETTINGS ==========
# Providers: "openai", "elevenlabs", "edge-tts" (Free)
VOICEOVER_PROVIDER = "edge-tts" 
VOICEOVER_VOICE = "en-US-ChristopherNeural" # Default for Edge-TTS

# ElevenLabs Settings
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM" # Rachael

# OpenAI TTS Settings
OPENAI_TTS_MODEL = "tts-1-hd"
OPENAI_TTS_VOICE = "onyx"

# ========== QUALITY SETTINGS ==========
QUALITY_MODE = "ultra"  # "draft", "standard", "high", "ultra"

QUALITY_PROFILES = {
    "draft": {
        "resolution": (1280, 720),
        "fps": 24,
        "bitrate": 4000,
        "preset": "fast"
    },
    "standard": {
        "resolution": (1920, 1080),
        "fps": 24,
        "bitrate": 8000,
        "preset": "medium"
    },
    "high": {
        "resolution": (1920, 1080),
        "fps": 30,
        "bitrate": 12000,
        "preset": "slow"
    },
    "ultra": {
        "resolution": (1920, 1080),
        "fps": 24,
        "bitrate": 16000,
        "preset": "slower",
        "color_depth": "10bit"
    }
}

# ========== API RETRY SETTINGS ==========
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# ========== FEATURE FLAGS ==========
ENABLE_VOICEOVER = True  # Re-enabled with new Premium Agent
ENABLE_COMFYUI = True  # Enabled for advanced video gen
ENABLE_OFFLINE_FALLBACK = True  # Generate placeholders if APIs fail
ENABLE_QUALITY_LOOPS = True  # Super Director review loops
ENABLE_MULTI_API = True  # Use multiple AI APIs with fallback

# Create directories if they don't exist
for directory in [OUTPUT_DIR, ASSETS_DIR, WORKFLOWS_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

print(f"✅ Config loaded - Quality mode: {QUALITY_MODE}")
if ANTHROPIC_API_KEY:
    print("✅ Claude Sonnet 4 available (Premium)")
if OPENAI_API_KEY:
    print("✅ GPT-4 available")
if GROQ_API_KEY:
    print("✅ Groq available")
