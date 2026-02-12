import os
import json
import time
from comfy_client import ComfyClient
from config import WORKFLOWS_DIR, OUTPUT_DIR

class ArtDeptAgent:
    def __init__(self, auto_start_comfy=True):
        # Initialize ComfyUI with auto-start
        self.comfy = ComfyClient(auto_start=auto_start_comfy)
        self.ltx2_available = False
        self.ltx2_pipeline = None
        
        # Try to load LTX-2
        try:
            from agents.ltx2_video import LTX2VideoAgent
            self.ltx2 = LTX2VideoAgent()
            self.ltx2_available = True
            print("   🎬 LTX-2 video generation: Available")
        except Exception as e:
            print(f"   ⚠️ LTX-2 not available: {e}")
            self.ltx2 = None
        
        # Load the Flux workflow template
        workflow_path = os.path.join(WORKFLOWS_DIR, "flux_workflow_api.json")
        if os.path.exists(workflow_path):
            with open(workflow_path, 'r') as f:
                self.flux_template = json.load(f)
        else:
            print(f"⚠️ Warning: Workflow NOT found at {workflow_path}")
            self.flux_template = {}

    def generate_video_clip(self, scene_data, duration=5):
        """
        Generate video clip with intelligent fallback:
        1. Try LTX-2 (AI generation)
        2. Try ComfyUI (if connected)
        3. Fall back to stock footage
        
        Args:
            scene_data: Scene dictionary with visual_prompt
            duration: Clip duration in seconds
        
        Returns:
            Path to generated video or None (triggers stock fallback)
        """
        prompt = scene_data.get('visual_prompt', '')
        
        # Strategy 1: LTX-2 AI generation (preferred for custom content)
        if self.ltx2_available and self._should_use_ltx2(scene_data):
            print(f"   🎬 Strategy: LTX-2 AI Generation")
            result = self.ltx2.generate_video(
                prompt=prompt,
                duration=duration,
                width=512,
                height=384
            )
            if result:
                return result
            print("   ⚠️ LTX-2 failed, trying ComfyUI...")
        
        # Strategy 2: ComfyUI (if connected)
        if self.comfy.connected:
            print(f"   🎬 Strategy: ComfyUI Generation")
            result = self.generate_keyframe(scene_data)
            if result:
                return result
            print("   ⚠️ ComfyUI failed, falling back to stock...")
        
        # Strategy 3: Stock footage (handled by caller)
        print("   🎬 Strategy: Stock Footage Fallback")
        return None
    
    def _should_use_ltx2(self, scene_data):
        """Decide if scene should use LTX-2 generation"""
        source_type = scene_data.get('source_type', 'STOCK')
        prompt = scene_data.get('visual_prompt', '').lower()
        
        # Use LTX-2 for:
        # - Scenes marked as GENERATE
        # - Brand-specific content
        # - Custom/unique requirements
        if source_type == 'GENERATE':
            return True
        
        brand_keywords = ['brand', 'logo', 'custom', 'specific product']
        if any(kw in prompt for kw in brand_keywords):
            return True
        
        return False

    def generate_keyframe(self, scene_data):
        """
        Generates a keyframe image via ComfyUI. Returns filename.
        """
        if not self.comfy.connected:
            print("   ⚠️ Art Dept: ComfyUI not connected. Skipping generation.")
            return None

        prompt_text = scene_data.get('visual_prompt', "")
        print(f"   🎨 Generating Keyframe: '{prompt_text[:50]}...'")
        
        try:
            # Clone template
            workflow = self.flux_template.copy()
            
            # Inject Prompt (Node ID 6 is CLIP Text Encode)
            if "6" in workflow:
                workflow["6"]["inputs"]["text"] = prompt_text
            
            # Queue Prompt
            response = self.comfy.queue_prompt(workflow)
            prompt_id = response['prompt_id']
            
            # Wait for completion (Simple Polling)
            print("      ⏳ Rendering...")
            time.sleep(5) # Placeholder wait
            
            return f"flux_{prompt_id}.png"
            
        except Exception as e:
            print(f"   ❌ Art Dept Error: {e}")
            return None
