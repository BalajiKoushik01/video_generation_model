import os
import json
import requests
import urllib3
from config import GROQ_API_KEY, LLM_MODEL

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ScreenwriterAgent:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.model = LLM_MODEL

    def write_script(self, user_prompt):
        """
        Generates GEMINI VEO-LEVEL cinema-quality scripts.
        """
        from agents.llm_client import LLMClient
        client = LLMClient()

        if client.provider == "ollama":
            # Ultra-Simplified Prompt for Local Models (Llama3)
            system_prompt = """You are a script writer.
Reply with JSON only.
{
  "scenes": [
    {
      "visual_prompt": "description of a video shot",
      "duration": 5
    }
  ]
}
"""
        else:
            # Full Cinematic Prompt for Cloud Models
            system_prompt = """You are a WORLD-CLASS Creative Director creating GEMINI VEO-LEVEL video advertisements.

🎯 MISSION: Generate scripts so detailed and cinematic they produce STUNNING videos.

📐 STRUCTURE:
- Duration: 25-30 seconds
- Shots: 6-7 scenes (4-5s each)
- Arc: Hook → Build → Climax → Resolution

🎬 FOR EACH SHOT PROVIDE:

**VISUAL DESCRIPTION** (Ultra-Detailed):
- Shot type: EXTREME CLOSE-UP / CLOSE-UP / MEDIUM / WIDE / AERIAL
- Subject details: Texture, color, form, specific elements
- Composition: Rule of thirds, leading lines, depth
- Lighting: Golden hour / Rembrandt / High-key / Natural window / Dramatic side
- Color palette: Warm/cool tones
- Atmosphere: Steam, mist, bokeh, reflections
- Premium details that make it memorable

**CAMERA SPECS**:
- Camera: Arri Alexa / RED Komodo / Sony FX6
- Lens: 24mm wide / 50mm prime / 85mm portrait
- Aperture: f/1.4 / f/2.8 / f/5.6
- Frame rate: 24fps / 60fps slow-motion

**CAMERA MOVEMENT**:
- Dolly: Slow push-in / pull-out
- Crane: Rise / descend for reveal
- Gimbal: Smooth tracking
- Handheld: Intimate feel
- Static: Locked-off
- Slider: Lateral parallax

**EMOTIONAL INTENT**:
- Feeling: warmth / luxury / excitement / peace
- Story contribution
- Narrative building

**SOURCE** (CRITICAL):
- Use "STOCK" for 90% of shots
- Use "GENERATE" ONLY for: branded elements, impossible scenarios
- When uncertain → STOCK

🌟 JSON FORMAT:
{
  "scenes": [
    {
      "visual_prompt": "[SHOT TYPE]: [Detailed subject] shot with [Camera+Lens], [composition], [lighting mood], [atmosphere], [colors]",
      "text_overlay": "[Brief catchy text/slogan for this shot, or empty]",
      "voiceover": "[Compelling narration, 1-2 sentences]",
      "duration": 5
    }
  ]
}

✅ QUALITY STANDARDS:
- Every frame is art
- Intentional lighting
- Classic composition
- Movement serves story
- Harmonious colors
- Clear emotional arc
- Lasting final impression

EXAMPLE OF EXCELLENCE:
❌ BAD: "Coffee cup on table"
✅ GOOD: "EXTREME CLOSE-UP: Weathered hands cradling white ceramic cup, steam wisps rising, Arri Alexa + 85mm f/1.4, shallow DOF, soft window light camera-left, warm minimalist kitchen, intimate mood"

Think: PREMIUM. ARTISTIC. MEMORABLE."""

        user_content = f"Create a GEMINI VEO-LEVEL 25-30 second video for: {user_prompt}"

        # Generate Script
        print(f"   ✍️ Screenwriter is writing ({client.provider})...")
        try:
            result = client.generate(system_prompt, user_content, temperature=0.9, json_mode=True)
            if not result:
                raise Exception("Empty response from LLM")
            return json.dumps(result) # Return as string for compatibility
        except Exception as e:
            print(f"   ⚠️ Screenwriter Error: {e}")
            import traceback
            traceback.print_exc()
            raise e

    def _clean_json(self, text):
        """Removes Markdown formatting"""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
