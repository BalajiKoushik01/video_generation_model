"""
Master AI Director - Top-level intelligent orchestrator
Uses Claude/GPT-4 to plan, control, and optimize the entire production workflow
"""
import os
import json
import requests
from config import GROQ_API_KEY

class MasterDirector:
    """
    Master AI that intelligently controls the entire video production workflow.
    Makes high-level creative decisions and ensures quality.
    """
    def __init__(self):
        self.api_key = GROQ_API_KEY
        # Using Llama 3.3 70B for now, can upgrade to Claude/GPT-4
        self.model = "llama-3.3-70b-versatile"
        
    def plan_production(self, user_brief):
        """
        Master-level planning: Creates detailed production plan with shot sequences,
        timing, transitions, and quality requirements.
        """
        print("🎬 MASTER DIRECTOR: Analyzing brief and creating production plan...")
        
        prompt = f"""You are a Master Film Director with decades of experience in advertising.
        
USER BRIEF: {user_brief}

Create a DETAILED production plan with:

1. CREATIVE VISION (2-3 sentences describing the emotional arc and style)

2. SHOT SEQUENCE (5-7 shots with EXACT timing):
   - Shot number and duration (3-6 seconds each)
   - Visual description (what we see)
   - Camera specs (lens, movement, lighting)
   - Crop/trim instructions (if stock footage needs editing)
   - Transition type (cut, fade, dissolve)
   - Voiceover text (what narrator says during this shot)
   - Music cue (intensity: low/medium/high)

3. PACING GUIDE:
   - Which shots are fast-paced (high energy)
   - Which shots are slow (emotional beats)
   - Where to build tension
   - Where the payoff/climax happens

4. AUDIO MIX:
   - Voiceover volume level per shot (0-100%)
   - Music volume per shot (0-100%)
   - Sound effects needed and when

5. QUALITY CHECKLIST:
   - Must-have visual elements
   - Emotional beats to hit
   - Brand message clarity

OUTPUT AS JSON with this structure:
{{
  "creative_vision": "...",
  "total_duration": 25,
  "shots": [
    {{
      "number": 1,
      "duration": 4,
      "visual": "...",
      "camera": "...",
      "crop_instructions": "Crop to 16:9, focus center, trim to 4s",
      "transition_to_next": "fade",
      "voiceover": "...",
      "vo_volume": 100,
      "music_intensity": "low",
      "music_volume": 40,
      "sound_effects": ["coffee pour", "ambient cafe"],
      "sfx_volume": 30,
      "pacing": "slow"
    }}
  ],
  "quality_goals": ["...", "..."]
}}

CRITICAL: Create a 25-30 second ad that tells a complete story with emotional impact.
Use cinematic language and precise timing."""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an award-winning Master Director. Always output valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 3000,
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                verify=False,
                timeout=30
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                plan = json.loads(content)
                
                print(f"\n✅ PRODUCTION PLAN COMPLETE")
                print(f"   Vision: {plan.get('creative_vision', 'N/A')}")
                print(f"   Total Duration: {plan.get('total_duration', 0)}s")
                print(f"   Shots Planned: {len(plan.get('shots', []))}")
                
                return plan
            else:
                print(f"❌ Master Director Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Master Director Exception: {e}")
            return None
    
    def review_quality(self, assets, script):
        """
        Master-level quality review: Ensures the production meets standards.
        """
        print("🎯 MASTER DIRECTOR: Conducting quality review...")
        
        issues = []
        recommendations = []
        
        # Check asset count
        if len(assets) < 5:
            issues.append("Too few clips (< 5) - may feel rushed")
            recommendations.append("Acquire more B-roll for variety")
        
        # Check durations
        total_duration = sum(s.get('duration', 0) for s in script.get('shots', []))
        if total_duration < 20:
            issues.append(f"Too short ({total_duration}s) - needs to be 25-30s")
        elif total_duration > 35:
            issues.append(f"Too long ({total_duration}s) - trim to 25-30s")
        
        # Check voiceover presence
        has_vo = any(s.get('voiceover') for s in script.get('shots', []))
        if not has_vo:
            issues.append("No voiceover - ads need narration")
            recommendations.append("Add voiceover to key shots")
        
        quality_score = max(0, 100 - (len(issues) * 15))
        
        print(f"\n   Quality Score: {quality_score}/100")
        if issues:
            print(f"   ⚠️ Issues Found:")
            for issue in issues:
                print(f"      - {issue}")
        if recommendations:
            print(f"   💡 Recommendations:")
            for rec in recommendations:
                print(f"      - {rec}")
        
        return {
            "score": quality_score,
            "issues": issues,
            "recommendations": recommendations,
            "approved": quality_score >= 70
        }
    
    def optimize_pacing(self, shots):
        """
        Intelligent pacing optimization - ensures good rhythm and flow.
        """
        print("⚡ MASTER DIRECTOR: Optimizing pacing and rhythm...")
        
        # Ensure alternating pace for engagement
        optimized = []
        for i, shot in enumerate(shots):
            pace = shot.get('pacing', 'medium')
            
            # Alternate fast/slow for rhythm
            if i > 0:
                prev_pace = optimized[-1].get('pacing', 'medium')
                if prev_pace == 'fast' and pace == 'fast':
                    shot['pacing'] = 'medium'  # Slow down
                elif prev_pace == 'slow' and pace == 'slow':
                    shot['pacing'] = 'medium'  # Speed up
            
            optimized.append(shot)
        
        return optimized
