import os
import json
import time
import urllib.request
import urllib.parse
import uuid
import threading
try:
    import websocket # Requires websocket-client
except ImportError:
    websocket = None

from config import COMFYUI_HOST, COMFYUI_PORT, OUTPUT_DIR, VIDEO_MODEL, WORKFLOWS_DIR

class ProductionAgent:
    def __init__(self):
        self.server_address = f"{COMFYUI_HOST}:{COMFYUI_PORT}"
        self.client_id = str(uuid.uuid4())
        print(f"🎬 Production Agent initialized (Video Model: {VIDEO_MODEL})")
        
    def shoot_scene(self, scene_data, keyframe_path=None):
        """
        Generates a video clip for the scene using ComfyUI.
        """
        # If no keyframe, we can't do image-to-video efficiently yet without more complex workflows
        # But for now let's assume we might generate T2V if no keyframe, or I2V if keyframe exists.
        
        prompt = scene_data.get('visual_prompt', '')
        duration = scene_data.get('duration', 4)
        print(f"   🎥 Shooting Scene: '{prompt[:40]}...' ({duration}s)")
        
        if not self._check_comfyui_connection():
            print("   ⚠️ ComfyUI not reachable. Creating placeholder.")
            return self._create_placeholder(prompt)
            
        # 1. Load Workflow
        workflow = self._load_workflow(VIDEO_MODEL)
        if not workflow:
            return self._create_placeholder(prompt)
            
        # 2. Update Workflow with Prompt
        workflow = self._prepare_workflow(workflow, prompt, keyframe_path, duration)
        
        # 3. Queue Prompt
        print("      🚀 Sending to ComfyUI...")
        try:
            prompt_id = self._queue_prompt(workflow)
            
            # 4. Wait for completion (with timeout)
            video_filename = self._wait_for_completion(prompt_id)
            
            if video_filename:
                # Move to output dir if not already there (ComfyUI saves to its own output usually)
                # But our helper returns the filename in ComfyUI output. 
                # We need to find the file.
                return self._retrieve_video(video_filename)
        except Exception as e:
            print(f"      ❌ ComfyUI Error: {e}")
            
        return self._create_placeholder(prompt)
        
    def _check_comfyui_connection(self):
        try:
            url = f"http://{self.server_address}/system_stats"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                return response.status == 200
        except:
            return False

    def _load_workflow(self, model_name):
        filename = f"{model_name}_workflow_api.json"
        path = os.path.join(WORKFLOWS_DIR, filename)
        if not os.path.exists(path):
            print(f"      ❌ Workflow file not found: {path}")
            return None
            
        with open(path, 'r') as f:
            return json.load(f)
            
    def _prepare_workflow(self, workflow, prompt, keyframe, duration):
        # This is heuristics-based modification of the API JSON
        # We look for nodes that look like they take text or images
        
        for node_id, node in workflow.items():
            inputs = node.get("inputs", {})
            class_type = node.get("class_type", "")
            
            # Update Prompt
            if class_type in ["CLIPTextEncode", "HunyuanVideoPrompt"]:
                if "text" in inputs:
                    inputs["text"] = prompt
            
            # Update Image (if Keyframe provided and node expects image)
            if keyframe and class_type == "LoadImage":
                # ComfyUI usually expects image in input folder. config.ASSETS_DIR? 
                # For now, we assume user must manually put it there or we copy it.
                # Actually, specialized nodes need full paths or relative to input.
                # Simplest hack: Copy keyframe to ComfyUI input folder? 
                # For this implementation, we will assume T2V for now unless we implement proper upload.
                pass 
                
        return workflow

    def _queue_prompt(self, workflow):
        p = {"prompt": workflow, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        url = f"http://{self.server_address}/prompt"
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read())['prompt_id']

    def _wait_for_completion(self, prompt_id):
        if websocket is None:
            print("      ⚠️ WebSocket lib missing. Waiting blindly (30s)...")
            time.sleep(30)
            return None # Can't know filename without WS
            
        ws = websocket.WebSocket()
        ws.connect(f"ws://{self.server_address}/ws?clientId={self.client_id}")
        
        print("      ⏳ Rendering...")
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        # Execution finished
                        break
        
        # Get history to find output filename
        with urllib.request.urlopen(f"http://{self.server_address}/history/{prompt_id}") as response:
            history = json.loads(response.read())[prompt_id]
            outputs = history['outputs']
            
            # Extract video filename from outputs
            for node_id, output_data in outputs.items():
                if 'gifs' in output_data:
                    return output_data['gifs'][0]['filename']
                if 'videos' in output_data:
                    return output_data['videos'][0]['filename']
        return None

    def _retrieve_video(self, filename):
        # We need to compute where ComfyUI saved it. 
        # Usually defaults to ComfyUI/output.
        # We will attempt to find it or download it from view endpoint
        
        url = f"http://{self.server_address}/view?filename={filename}&type=output"
        
        # Save to our output dir
        target_path = os.path.join(OUTPUT_DIR, filename)
        urllib.request.urlretrieve(url, target_path)
        return target_path

    def _create_placeholder(self, prompt):
        # Simply return None so the system knows to skip or use static image
        return None
