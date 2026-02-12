import os
from huggingface_hub import hf_hub_download

def download_file(repo_id, filename, target_dir):
    print(f"⬇️ Downloading {filename} from {repo_id}...")
    try:
        path = hf_hub_download(repo_id=repo_id, filename=filename, local_dir=target_dir, local_dir_use_symlinks=False)
        print(f"   ✅ Saved to {path}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")

import subprocess

if __name__ == "__main__":
    print("🎬 Hollywood Studio Model Setup 🎬")
    print("This script will download the required AI models (approx 20GB).")
    
    # Determine Project Root
    TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(TOOLS_DIR)
    comfy_path = os.path.join(PROJECT_ROOT, "ComfyUI")
    
    # Auto-Install ComfyUI if missing
    if not os.path.exists(comfy_path):
        print(f"📦 ComfyUI not found. Cloning to {comfy_path}...")
        try:
            subprocess.run(["git", "clone", "https://github.com/comfyanonymous/ComfyUI.git", comfy_path], check=True)
            print("   ✅ ComfyUI Cloned.")
        except Exception as e:
            print(f"   ❌ Git Clone Failed: {e}")
            print("   Please install ComfyUI manually and try again.")
            exit()
    else:
        print(f"   ✅ Found ComfyUI at {comfy_path}")
        
    # 1. Flux.1 Schnell (FP8 - Usually faster and public)
    # Using Kijai's FP8 builds which are highly optimized for ComfyUI
    ckpt_dir = os.path.join(comfy_path, "models", "checkpoints") # Fix path to include 'models'
    download_file("Kijai/flux-fp8", "flux1-schnell-fp8.safetensors", ckpt_dir)
    
    # 2. Hunyuan Video (Quantized for Consumer GPUs)
    # Using the GGUF or FP8 version. Let's try the standard FP8.
    download_file("Kijai/HunyuanVideo_comfy", "hunyuan_video_720_cfg_distill_fp8.safetensors", ckpt_dir)
    
    # 3. RealESRGAN
    upscale_dir = os.path.join(comfy_path, "models", "upscale_models")
    if not os.path.exists(upscale_dir): os.makedirs(upscale_dir)
    download_file("ai-forever/Real-ESRGAN", "RealESRGAN_x4plus.pth", upscale_dir)
    
    # 4. AudioCraft (MusicGen Main)
    # Checkpoints usually go in models/checkpoints or models/audiocraft depending on node
    # We will put it in checkpoints for now as many nodes look there
    download_file("facebook/musicgen-small", "state_dict.bin", os.path.join(comfy_path, "models", "checkpoints", "musicgen_small"))
    
    print("\n✅ All downloads triggered. If successful, restart ComfyUI to load them.")
