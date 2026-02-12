import json
from agents.llm_client import LLMClient

class CinematographerAgent:
    """
    Specialized Agent: The Director of Photography (DP).
    Responsibilities:
    - Takes a narrative script.
    - Rewrites 'visual_prompt' into technical camera instructions.
    - Ensures visual consistency (color palette, lighting style).
    """
    def __init__(self):
        self.llm = LLMClient()

    def enhance_visuals(self, script_data):
        print("   🎥 Cinematographer: Enhancing visual prompts...")
        
        scenes = script_data.get('scenes', [])
        if not scenes:
            return script_data

        enhanced_scenes = []
        
        for i, scene in enumerate(scenes):
            original_visual = scene.get('visual_prompt', '')
            print(f"      👁️ Analyzing Scene {i+1}: {original_visual[:40]}...")
            
            # Specialized System Prompt for the DP
            system_prompt = """You are a Master Cinematographer (DoP).
Your job is to translate a script description into a Technical Visual Prompt for an AI Video Generator.

Input: "A man showing a coffee cup."
Output: "Close-up shot of a ceramic coffee cup held by weathered hands, 50mm lens, f/1.8, soft morning lighting, steam rising, bokeh kitchen background, high resolution, photorealistic."

RULES:
1. Be specific about CAMERA ANGLE (Low angle, Overhead, Eye level).
2. Specify LIGHTING (Golden hour, Neon, Studio softbox).
3. Specify LENS/STYLE (Wide angle, Macro, 35mm film grain).
4. Keep it under 40 words.
5. Return ONLY the prompt text. No quotes."""

            try:
                # We use a lower temperature for consistent technical details
                technical_prompt = self.llm.generate(
                    system_prompt=system_prompt,
                    user_prompt=f"Enhance this visual: {original_visual}",
                    temperature=0.6,
                    json_mode=False
                )
                
                # Check validity
                if technical_prompt and len(technical_prompt) > 5:
                    scene['visual_prompt'] = technical_prompt.strip()
                    print(f"         ✨ Enhanced: {technical_prompt[:50]}...")
                else:
                    print("         ⚠️ Enhancement failed, keeping original.")
                    
            except Exception as e:
                print(f"         ❌ Cinematographer error: {e}")
            
            enhanced_scenes.append(scene)
            
        script_data['scenes'] = enhanced_scenes
        return script_data
