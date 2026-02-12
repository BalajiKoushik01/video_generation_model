"""
Enhanced ComfyUI Client with Auto-Start and LTX-Video Support
Integrates ComfyUI server management and workflow execution
"""
import os
import sys
import json
import time
import requests
import websocket
import subprocess
import threading
from pathlib import Path
from config import COMFYUI_HOST, COMFYUI_PORT

class ComfyClient:
    """
    ComfyUI client with automatic server management and LTX-Video support.
    """
    def __init__(self, auto_start=False):
        self.host = COMFYUI_HOST
        self.port = COMFYUI_PORT
        self.url = f"http://{self.host}:{self.port}"
        self.ws_url = f"ws://{self.host}:{self.port}/ws"
        self.connected = False
        self.server_process = None
        
        # Check if ComfyUI is installed
        self.comfy_dir = Path(__file__).parent / "ComfyUI"
        self.comfy_installed = self.comfy_dir.exists()
        
        # Try to connect
        self._check_connection()
        
        # Auto-start if requested and not connected
        if auto_start and not self.connected and self.comfy_installed:
            self.start_server()
    
    def _check_connection(self):
        """Check if ComfyUI server is running"""
        try:
            response = requests.get(f"{self.url}/system_stats", timeout=2)
            self.connected = (response.status_code == 200)
            if self.connected:
                print(f"   ✅ ComfyUI connected at {self.url}")
        except:
            self.connected = False
    
    def start_server(self, wait_time=10):
        """
        Start ComfyUI server in background.
        
        Args:
            wait_time: Seconds to wait for server startup
        """
        if not self.comfy_installed:
            print("   ⚠️ ComfyUI not installed. Run: python setup_comfyui.py")
            return False
        
        if self.connected:
            print("   ✅ ComfyUI already running")
            return True
        
        print(f"   🚀 Starting ComfyUI server...")
        
        try:
            # Start ComfyUI in background
            main_py = self.comfy_dir / "main.py"
            
            self.server_process = subprocess.Popen(
                [sys.executable, str(main_py), "--listen"],
                cwd=str(self.comfy_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
            )
            
            print(f"   ⏳ Waiting {wait_time}s for server startup...")
            time.sleep(wait_time)
            
            # Check connection
            self._check_connection()
            
            if self.connected:
                print(f"   ✅ ComfyUI server started successfully!")
                return True
            else:
                print(f"   ⚠️ Server may still be starting. Check manually at {self.url}")
                return False
                
        except Exception as e:
            print(f"   ❌ Failed to start ComfyUI: {e}")
            return False
    
    def stop_server(self):
        """Stop ComfyUI server"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
            self.connected = False
            print("   🛑 ComfyUI server stopped")
    
    def queue_prompt(self, workflow):
        """
        Queue a workflow for execution.
        
        Args:
            workflow: Dict containing ComfyUI workflow
        
        Returns:
            Response dict with prompt_id
        """
        if not self.connected:
            raise Exception("ComfyUI not connected")
        
        # Prepare prompt
        prompt_data = {
            "prompt": workflow,
            "client_id": "hollywood_studio"
        }
        
        # Send to ComfyUI
        response = requests.post(
            f"{self.url}/prompt",
            json=prompt_data,
            verify=False
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"ComfyUI error: {response.status_code}")
    
    def get_history(self, prompt_id):
        """Get execution history for a prompt"""
        if not self.connected:
            return None
        
        response = requests.get(f"{self.url}/history/{prompt_id}")
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_output_path(self, prompt_id, output_dir="output"):
        """
        Get path to generated output.
        
        Args:
            prompt_id: The prompt ID from queue_prompt
            output_dir: Output directory name
        
        Returns:
            Path to output file or None
        """
        history = self.get_history(prompt_id)
        if not history or prompt_id not in history:
            return None
        
        outputs = history[prompt_id].get('outputs', {})
        for node_id, node_output in outputs.items():
            if 'images' in node_output:
                images = node_output['images']
                if images:
                    filename = images[0]['filename']
                    return os.path.join(self.comfy_dir, output_dir, filename)
        
        return None
    
    def wait_for_completion(self, prompt_id, max_wait=120, check_interval=2):
        """
        Wait for workflow execution to complete.
        
        Args:
            prompt_id: The prompt ID to wait for
            max_wait: Maximum wait time in seconds
            check_interval: Seconds between status checks
        
        Returns:
            True if completed, False if timeout
        """
        waited = 0
        while waited < max_wait:
            history = self.get_history(prompt_id)
            
            if history and prompt_id in history:
                status = history[prompt_id].get('status', {})
                if status.get('completed', False):
                    return True
            
            time.sleep(check_interval)
            waited += check_interval
        
        return False
