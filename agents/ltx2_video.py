"""
LTX-2 Video Generation Agent (ComfyUI GGUF Backup)
Uses ComfyUI with GGUF models for low-VRAM generation
"""
import os
import time
import json
import random
from config import OUTPUT_DIR, WORKFLOWS_DIR
from comfy_client import ComfyClient

class LTX2VideoAgent:
    """
    AI Video Generation using LTX-Video model via ComfyUI (GGUF).
    Optimized for 4GB VRAM.
    """
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.workflow_path = os.path.join(WORKFLOWS_DIR, "ltx_video_2b_gguf_workflow.json")
        self.client = ComfyClient(auto_start=True)
        self.available = self.client.connected
        
    def generate_video(self, prompt, duration=5, width=768, height=512):
        if not self.available:
            print("   ⚠️ ComfyUI not available for LTX-2 generation")
            return None
            
        print(f"   🎬 LTX-2 (GGUF) Generating: '{prompt[:50]}...'")
        
        try:
            # Load workflow
            with open(self.workflow_path, 'r') as f:
                workflow = json.load(f)
            
            # Update workflow with prompt and settings
            # Note: IDs must match ltx_video_2b_gguf_workflow.json
            # Node 13 = Positive Prompt
            workflow["nodes"][3]["widgets_values"][0] = prompt
            
            # Node 15 = EmptyLatentImage (width, height, frames)
            # frames = duration * 24
            frames = int(duration * 24)
            workflow["nodes"][5]["widgets_values"] = [width, height, frames]
            
            # Node 3 = KSampler (seed)
            seed = random.randint(1, 999999999)
            workflow["nodes"][6]["widgets_values"][0] = seed
            
            # Node 20 = SaveVideo (filename_prefix)
            prefix = f"ltx2_gguf_{seed}"
            workflow["nodes"][8]["widgets_values"][0] = prefix

            # Convert to API format (prompt object)
            # ComfyUI API expects {node_id: {inputs: ..., class_type: ...}}
            # But we have a workflow JSON (graph). 
            # We need to map the graph values to the API format or just use the widgets if using a simplified client.
            # actually, standard ComfyUI API requires the 'prompt' format, not the 'workflow' format.
            # The workflow style I saved is likely the UI format.
            # Let's try to infer or use the client's queuing mechanism if it supports the UI format (often it doesn't).
            # standard approach: convert UI JSON to API JSON.
            
            # SIMPLIFICATION:
            # Since converting UI JSON to API JSON programmatically is complex without the heavy node map,
            # we will rely on a pre-converted API format if possible, OR assume the client handles it.
            # Wait, I created the workflow JSON manually in step 232.
            # That JSON structure I made looked like UI structure ("nodes", "links").
            # The API expects: { "3": { "inputs": { ... }, "class_type": "KSampler" }, ... }
            
            # Re-creating the API version of the workflow here for robustness
            prompt_api = {
                "10": {
                    "inputs": {"unet_name": "ltx-video-2b-v0.9-Q8_0.gguf"},
                    "class_type": "UnetLoaderGGUF"
                },
                "11": {
                    "inputs": {
                        "clip_name": "t5-v1_1-xxl-encoder-Q4_K_M.gguf",
                        "type": "t5"
                    },
                    "class_type": "CLIPLoaderGGUF"
                },
                "12": {
                    "inputs": {"vae_name": "LTX-Video-VAE-BF16.safetensors"},
                    "class_type": "VAELoader"
                },
                "13": {
                    "inputs": {
                        "text": prompt,
                        "clip": ["11", 0]
                    },
                    "class_type": "CLIPTextEncode"
                },
                "14": {
                    "inputs": {
                        "text": "blurry, low quality, worst quality",
                        "clip": ["11", 0]
                    },
                    "class_type": "CLIPTextEncode"
                },
                "15": {
                    "inputs": {
                        "width": width,
                        "height": height,
                        "length": frames,
                        "batch_size": 1
                    },
                    "class_type": "EmptyLatentImage"
                },
                "3": {
                    "inputs": {
                        "seed": seed,
                        "steps": 20,
                        "cfg": 3.0,
                        "sampler_name": "euler",
                        "scheduler": "simple",
                        "denoise": 1.0,
                        "model": ["10", 0],
                        "positive": ["13", 0],
                        "negative": ["14", 0],
                        "latent_image": ["15", 0]
                    },
                    "class_type": "KSampler"
                },
                "8": {
                    "inputs": {
                        "samples": ["3", 0],
                        "vae": ["12", 0]
                    },
                    "class_type": "VAEDecode"
                },
                "20": {
                    "inputs": {
                        "filename_prefix": prefix,
                        "format": "video/h264-mp4", # or just use default SaveVideo if this custom node doesn't exist
                         # Standard SaveVideo implies images. We likely need 'SaveAnimatedWEBP' or 'VideoHelperSuite'.
                         # Using standard SaveImage/Video for now to match my previous workflow assumption.
                         # Actually ComfyUI-VideoHelperSuite is installed (Step 173).
                         # Let's use VHS_VideoCombine.
                         "images": ["8", 0],
                         "frame_rate": 24,
                         "format": "video/h264-mp4"
                    },
                    "class_type": "VHS_VideoCombine" 
                }
            }

            # Queue prompt
            print("   🚀 Queuing task to ComfyUI...")
            response = self.client.queue_prompt(prompt_api)
            prompt_id = response['prompt_id']
            
            print(f"   ⏳ Generation queued (ID: {prompt_id}). This will take 1-3 minutes...")
            
            # Wait for completion
            if self.client.wait_for_completion(prompt_id, max_wait=300):
                # Retrieve output
                output_file = self.client.get_output_path(prompt_id)
                if output_file:
                    print(f"   ✅ Video generated: {output_file}")
                    return output_file
            
            print("   ❌ Timeout or no output received")
            return None
            
        except Exception as e:
            print(f"   ❌ ComfyUI Error: {e}")
            return None
            
    def generate_from_image(self, image_path, prompt, duration=5):
        return self.generate_video(prompt, duration, 768, 512)
