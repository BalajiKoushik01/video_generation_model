<<<<<<< HEAD
# 🎬 Hollywood Studio - AI Video Generation Pipeline

An advanced AI-powered video production system that orchestrates multiple specialized AI agents to create professional-quality videos from text prompts. Features a hierarchical director system, stock footage integration, AI video generation, and comprehensive post-production capabilities.

## ✨ Features

- **🎯 Multi-Agent Architecture**: Super Director + 5 Specialist Directors (Lighting, Cinematography, Editing, Transitions, Audio)
- **🤖 25+ Specialized AI Agents**: Screenwriter, Cinematographer, Editor, Sound Designer, Color Grading, and more
- **🎥 Dual Video Generation**: 
  - Stock footage from Pexels/Pixabay
  - AI-generated videos via ComfyUI (LTX-Video, Hunyuan)
- **🎙️ Professional Voiceover**: Edge-TTS (free), ElevenLabs, or OpenAI TTS
- **🎵 Audio Production**: AI music generation, sound effects, and mixing
- **🎨 Post-Production**: Color grading, transitions, text overlays, subtitles
- **💻 GUI & CLI**: User-friendly interface or command-line control
- **📊 Quality Modes**: Draft, Standard, High, Ultra (up to 1080p @ 24fps)

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (3.11 recommended)
- **Git** (for cloning repositories)
- **FFmpeg** (for video processing) - [Download here](https://ffmpeg.org/download.html)
- **Ollama** (optional, for local LLM) - [Download here](https://ollama.com/)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/BalajiKoushik01/AI_video-generation.git
   cd AI_video-generation
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Keys** (Edit `config.py`)
   - **Required**: `PEXELS_API_KEY` (free at [pexels.com/api](https://www.pexels.com/api/))
   - **Optional**: `GROQ_API_KEY`, `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`

5. **Setup ComfyUI** (for AI video generation)
   ```bash
   python setup_comfyui.py
   # OR
   setup_comfyui.bat
   ```

6. **Download Models** (if using local Ollama)
   ```bash
   ollama pull llama3
   ```

### Usage

#### GUI Mode (Recommended)
```bash
run_studio_gui.bat
# OR
python gui.py
```

#### CLI Mode
```bash
python studio.py
```

Then edit the script to add your prompt:
```python
if __name__ == "__main__":
    studio = HollywoodStudio()
    studio.produce_video("A cinematic coffee commercial with morning vibes")
```

#### Offline Mode (No API required)
```bash
run_offline.bat
```

## 📁 Project Structure

```
Hollywood_Studio/
├── studio.py              # Main orchestrator
├── gui.py                 # GUI interface
├── config.py              # Configuration & API keys
├── comfy_client.py        # ComfyUI integration
├── setup_comfyui.py       # ComfyUI installer
├── agents/                # AI Agent modules
│   ├── super_director.py
│   ├── screenwriter.py
│   ├── cinematographer.py
│   ├── editor.py
│   ├── voiceover.py
│   ├── sound_dept.py
│   └── ... (20+ more)
├── workflows/             # ComfyUI workflows
├── output/                # Generated videos (gitignored)
├── assets/                # Downloaded footage (gitignored)
└── ComfyUI/               # ComfyUI installation (gitignored)
```

## 🎨 Agent Architecture

### Hierarchical Director System
- **Super Director**: Chief creative officer, plans production strategy
- **Lighting Director**: Manages lighting and mood
- **Cinematography Director**: Camera angles, lenses, composition
- **Editing Director**: Pacing, cuts, transitions
- **Transitions Director**: Scene transitions and effects
- **Audio Director**: Music, voiceover, sound design

### Production Agents
- **Screenwriter**: Generates scene-by-scene scripts
- **Cinematographer**: Enhances visuals with lens/lighting specs
- **Art Department**: Generates AI images/keyframes
- **Smart Librarian**: Searches stock footage
- **Production**: Shoots scenes (AI video generation)
- **Editor**: Assembles final cut with audio sync
- **Sound Department**: Composes music
- **Sound Effects**: Adds ambient sounds
- **Color Grading**: Applies color palettes and LUTs
- **Voiceover**: Generates narration
- **Subtitles**: Auto-captions with Whisper
- **Marketing**: Creates press kits and posters

## ⚙️ Configuration

### Quality Modes (`config.py`)
```python
QUALITY_MODE = "ultra"  # "draft", "standard", "high", "ultra"
```

### LLM Provider
```python
LLM_PROVIDER = "ollama"  # "ollama", "groq", "anthropic", "openai"
```

### Video Generation
```python
VIDEO_MODEL = "hunyuan"  # "hunyuan" or "ltx2"
ENABLE_COMFYUI = True    # Set False to use stock footage only
```

### Voiceover Provider
```python
VOICEOVER_PROVIDER = "edge-tts"  # "edge-tts" (free), "elevenlabs", "openai"
```

## 🔧 Troubleshooting

### ComfyUI Not Connecting
1. Ensure ComfyUI is running: `cd ComfyUI && python main.py`
2. Check `http://127.0.0.1:8188` is accessible
3. Verify `COMFYUI_HOST` and `COMFYUI_PORT` in `config.py`

### No Audio in Output
- Check API keys in `config.py`
- Fallback music is included in `assets/fallback_music.mp3`
- Verify FFmpeg is installed: `ffmpeg -version`

### Stock Footage Not Found
- Verify `PEXELS_API_KEY` is set
- Check internet connection
- System will fallback to AI generation if stock fails

### Models Not Loading
- For Ollama: Run `ollama serve` in separate terminal
- For ComfyUI: Download models to `ComfyUI/models/` directories
- See `workflows/README_LTX_GGUF.txt` for model download links

## 📦 Dependencies

Large files/directories are excluded from Git via `.gitignore`:
- **ComfyUI/**: Install via `setup_comfyui.py`
- **assets/**: Auto-downloaded during video generation
- **output/**: Generated videos stored here
- **Models**: Download via setup scripts or Ollama

## 🎯 Example Prompts

```python
# Coffee Commercial
"A cinematic coffee commercial. Morning sunlight, steam rising, close-up of coffee beans."

# Tech Product
"Futuristic smartphone ad. Sleek design, holographic UI, city lights background."

# Travel Video
"Aerial shots of tropical beach. Turquoise water, palm trees, golden hour lighting."
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **ComfyUI** - Video generation framework
- **Pexels/Pixabay** - Stock footage providers
- **Ollama** - Local LLM runtime
- **Edge-TTS** - Free text-to-speech
- **MoviePy** - Video editing library

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review `config.py` for configuration options

---

**Made with ❤️ by the Hollywood Studio Team**
=======
# video_generation_model
>>>>>>> 3f12dd095b3630e3f4a56f427f6e1718fc337d44
