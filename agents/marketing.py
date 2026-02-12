import os
import json
from config import OUTPUT_DIR, LLM_PROVIDER
from agents.art_dept import ArtDeptAgent

class MarketingAgent:
    def __init__(self):
        print("   📢 Initializing Marketing Agent...")
        self.art_dept = ArtDeptAgent(auto_start_comfy=True)
        self.output_dir = os.path.join(OUTPUT_DIR, "PressKit")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def create_press_kit(self, script):
        """
        Generates a movie poster and social media marketing copy.
        """
        print("\n" + "="*50)
        print("📢 MARKETING AGENT: Assembling Press Kit")
        print("="*50)

        project_title = script.get("vision", "Untitled Project").split("\n")[0][:30]
        
        # 1. Generate Social Media Copy (LLM)
        print("   ✍️ Writing Social Media Campaign...")
        copy = self._generate_copy(script)
        
        copy_path = os.path.join(self.output_dir, "social_media.txt")
        with open(copy_path, "w", encoding="utf-8") as f:
            f.write(copy)
        print(f"   ✅ Copy saved: {copy_path}")

        # 2. Generate Poster (ComfyUI)
        print("   🎨 Designing Movie Poster...")
        poster_path = self._generate_poster(script)
        
        if poster_path:
            print(f"   ✅ Poster saved: {poster_path}")
        else:
            print("   ⚠️ Poster generation failed.")

        return self.output_dir

    def _generate_copy(self, script):
        """Uses LLM to write marketing copy"""
        from config import OLLAMA_BASE_URL, OLLAMA_MODEL
        import requests

        prompt = f"""You are a Hollywood Marketing Executive.
Write a viral social media campaign for this video project:

VISION: {script.get('vision')}
STYLE: {script.get('style')}

OUTPUT FORMAT:
1. HEADLINE (Catchy, emojis)
2. INSTAGRAM CAPTION (Engaging, hashtags)
3. TWEET (Short, punchy)
4. YOUTUBE DESCRIPTION (SEO optimized)

Make it hype!"""

        # OLLAMA SUPPORT
        if LLM_PROVIDER == "ollama":
            try:
                payload = {
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                }
                response = requests.post(OLLAMA_BASE_URL, json=payload)
                if response.status_code == 200:
                    return response.json()['response']
            except:
                pass
        
        # Fallback / Cloud logic would go here (omitted for brevity as we focused on local)
        return "Marketing copy generation unavailable (Check LLM connection)."

    def _generate_poster(self, script):
        """Generates a vertical poster using ArtDept"""
        # Create a visual description for the poster
        visual_theme = script.get('vision', 'Cinematic movie poster')
        poster_prompt = f"Movie Poster, {visual_theme}, textless, high resolution, 8k, cinematic lighting, vertical aspect ratio"
        
        # Use ArtDept to generate
        # We need to hack the aspect ratio. ArtDept usually does 16:9.
        # But we can try to ask for it.
        # Actually ArtDept's generate_keyframe uses a workflow.
        # We might need a specialized method or just rely on the prompt + crop.
        
        # Ideally we'd modify the workflow to be 2:3 ratio (e.g. 512x768)
        # For now, let's just generate a keyframe and call it a poster.
        
        scene_data = {"visual_prompt": poster_prompt}
        filename = self.art_dept.generate_keyframe(scene_data)
        
        if filename:
            # Move/Rename to PressKit
            src = os.path.join(OUTPUT_DIR, filename)
            dst = os.path.join(self.output_dir, "Poster.png")
            
            # Rename if exists
            import shutil
            if os.path.exists(src):
                shutil.move(src, dst)
                return dst
                
        return None
