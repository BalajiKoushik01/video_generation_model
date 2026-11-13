# Video Generation Studio — experimental media pipeline

This repository is a Python project for coordinating script planning, footage selection, narration, image/video generation and editing. It includes specialist agent modules, a command-line orchestrator and GUI entry points.

**Status:** experimental. Outputs and setup depend on local tools, external services, model files and available hardware. The repository is not a one-click guaranteed commercial video-production service.

## Code map

| Path | Purpose |
| --- | --- |
| `studio.py` | Orchestrates a production run and its agent stages |
| `agents/` | Scriptwriting, visual sourcing, editing, narration and supporting modules |
| `gui.py` | GUI entry point |
| `config.py` | Provider selection, paths and runtime settings |
| `comfy_client.py` | Optional ComfyUI integration |
| `workflows/` | Workflow-related assets and notes |
| `requirements.txt` | Python packages |
| `run_*.bat` | Windows launch helpers |

## Before running

- Install a compatible Python environment and FFmpeg.
- Create an isolated virtual environment and install `requirements.txt`.
- Open `config.py` and **replace machine-specific absolute paths** for outputs, assets and workflows. Treat them as local development defaults, not portable installation instructions.
- Configure only the external providers you intend to use through environment variables. Do not commit keys.
- Optional ComfyUI and local-model workflows need separate model installation and hardware.

```bash
git clone https://github.com/BalajiKoushik01/video_generation_model.git
cd video_generation_model
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python studio.py
```

For desktop operation, inspect `gui.py` and the `run_studio_gui.bat` helper. An end-to-end run has not been verified in this documentation review.

## Content and production caveats

Verify usage rights for footage, music, generated images and voice assets. Do not publish a cloned person's voice or likeness without permission. Generated material requires a human review for factual accuracy, sound quality, continuity and artefacts.

## Known maintenance work

- Check provider, model, FFmpeg and ComfyUI availability and document a reproducible fully rendered example.
- Test each provider and fallback separately.
- Add reproducible integration tests and a dependency lock strategy.
- Keep experimental quality modes separate from observed output quality.

This README replaces unresolved Git merge-conflict text in the previous version; it does not claim that source-code issues elsewhere have been resolved.
