# Production and validation guide

This repository is an experimental multi-agent media production pipeline. It is not a verified one-click finished-video service.

## Execution paths
- `studio.py`: script, visual selection, soundtrack, narration and rendering orchestration.
- `gui.py`: desktop entry point.
- `config.py`: provider/environment configuration, optional local Ollama/ComfyUI and asset/output paths.
- `agents/`: provider integration, scriptwriter, editor, voiceover and media helpers.
- `workflows/`: ComfyUI workflow definitions, whose referenced models must be installed separately.

## Development checks
Run `python -m compileall -q agents config.py studio.py gui.py`. CI verifies syntax and portable output paths. These checks do not exercise paid APIs or generate a complete video.

## End-to-end acceptance checklist
1. Verify the chosen provider responds to the configured model and that all HTTP calls use valid TLS verification, timeouts and bounded retries.
2. Produce a structured script and confirm scene durations sum to the intended runtime.
3. Acquire legally licensed footage/music and record attribution and usage permissions.
4. Check missing/empty media responses and fallback paths separately.
5. Generate voiceover and check expressive timing, pronunciation, clipping and consent.
6. Render with FFmpeg and inspect resolution, video codec, aspect ratio, captions, audio mix, frame continuity and playback on mobile.
7. Save a reproducible report containing settings, inputs, outputs and failed stages. Do not claim quality metrics without observed results.

## Security note
The global suppression of urllib3's insecure-request warnings in `agents/screenwriter.py` has been removed. This does not certify every provider integration. Do not disable HTTPS verification to make an API call succeed.
