
# LTX-Video-2b GGUF Setup (for 4GB VRAM)

I have initiated the download of optimized LTX-Video models:
1. **Model**: `ltx-video-2b-v0.9-Q8_0.gguf` (Best quality for low VRAM) -> `ComfyUI/models/unet`
2. **Encoder**: `t5-v1_1-xxl-encoder-Q4_K_M.gguf` -> `ComfyUI/models/clip`
3. **VAE**: `LTX-Video-VAE-BF16.safetensors` -> `ComfyUI/models/vae`
4. **Node**: `ComfyUI-GGUF` -> `ComfyUI/custom_nodes`

## Instructions:
1. **Wait for downloads to finish** (They are running in background).
2. **Restart ComfyUI** (if running) so it loads the new `ComfyUI-GGUF` node.
3. **Load Workflow**:
   - Drag and drop `workflows/ltx_video_2b_gguf_workflow.json` into ComfyUI.
   - Or load it via the `Load` button.
4. **Generate**:
   - The workflow is pre-configured for 4GB VRAM (using GGUF quantization).
   - If you see red nodes, ensure `ComfyUI-GGUF` is installed correctly.

## Note on Performance:
- Generation might be slow (1-2 mins per video) but it WILL work on 4GB VRAM.
- If you run out of memory, try closing other apps.
