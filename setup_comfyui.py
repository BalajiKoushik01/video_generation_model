"""
ComfyUI Setup Script for Hollywood Studio
Downloads and configures ComfyUI with LTX-Video nodes
"""
import os
import subprocess
import sys

def run_command(cmd, cwd=None):
    """Run command and print output"""
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    return True

def main():
    print("=" * 60)
    print("🎨 ComfyUI Setup for Hollywood Studio")
    print("=" * 60)
    print()
    
    # Check if ComfyUI already exists
    comfy_dir = "ComfyUI"
    if os.path.exists(comfy_dir):
        print(f"✅ ComfyUI directory already exists: {comfy_dir}")
        print("   Skipping clone...")
    else:
        print("📦 Step 1: Cloning ComfyUI...")
        if not run_command("git clone https://github.com/comfyanonymous/ComfyUI.git"):
            print("❌ Failed to clone ComfyUI")
            return
        print("✅ ComfyUI cloned")
    
    print()
    print("📦 Step 2: Installing ComfyUI dependencies...")
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", cwd=comfy_dir):
        print("❌ Failed to install dependencies")
        return
    print("✅ Dependencies installed")
    
    print()
    print("📦 Step 3: Downloading LTX-Video ComfyUI nodes...")
    custom_nodes_dir = os.path.join(comfy_dir, "custom_nodes")
    os.makedirs(custom_nodes_dir, exist_ok=True)
    
    ltx_node_dir = os.path.join(custom_nodes_dir, "ComfyUI-LTXVideo")
    if os.path.exists(ltx_node_dir):
        print(f"✅ LTX-Video nodes already exist")
    else:
        if not run_command(
            "git clone https://github.com/Lightricks/ComfyUI-LTXVideo.git",
            cwd=custom_nodes_dir
        ):
            print("❌ Failed to clone LTX-Video nodes")
            return
        print("✅ LTX-Video nodes downloaded")
    
    print()
    print("📦 Step 4: Installing LTX-Video node requirements...")
    if os.path.exists(os.path.join(ltx_node_dir, "requirements.txt")):
        if not run_command(
            f"{sys.executable} -m pip install -r requirements.txt",
            cwd=ltx_node_dir
        ):
            print("⚠️ Some LTX node requirements may have failed")
    
    print()
    print("📁 Step 5: Creating model directories...")
    model_dirs = [
        os.path.join(comfy_dir, "models", "checkpoints"),
        os.path.join(comfy_dir, "models", "ltx-video"),
        os.path.join(comfy_dir, "models", "upscale_models"),
    ]
    for dir in model_dirs:
        os.makedirs(dir, exist_ok=True)
        print(f"   ✅ Created: {dir}")
    
    print()
    print("=" * 60)
    print("✅ ComfyUI Setup Complete!")
    print("=" * 60)
    print()
    print("📋 Next Steps:")
    print("   1. Copy LTX-2 models to ComfyUI/models/ltx-video/")
    print("   2. Start ComfyUI server:")
    print(f"      $ cd {comfy_dir}")
    print(f"      $ {sys.executable} main.py")
    print("   3. Access at: http://127.0.0.1:8188")
    print()
    print("🎬 Hollywood Studio will auto-connect when ComfyUI is running!")
    print("=" * 60)

if __name__ == "__main__":
    main()
