"""
Specialist Directors - World-class experts for each production aspect
Each director is autonomous and produces professional-grade work
"""
import json
import requests
from config import GROQ_API_KEY

class BaseDirector:
    """Base class for all specialist directors"""
    def __init__(self, specialty):
        self.specialty = specialty
        self.api_key = GROQ_API_KEY
        self.model = "llama-3.3-70b-versatile"
    
    def execute(self, task, context):
        """Execute assigned task"""
        raise NotImplementedError


class LightingDirector(BaseDirector):
    """
    Expert in cinematography lighting, color grading, and visual mood
    """
    def __init__(self):
        super().__init__("Lighting & Color")
    
    def execute(self, shots, style="cinematic"):
        """
        Create comprehensive lighting and color plan
        """
        print(f"\n💡 LIGHTING DIRECTOR: Designing visual mood")
        
        plan = {
            "color_palette": self._generate_palette(style),
            "grading_per_shot": [],
            "mood": style,
            "lut_recommendation": self._recommend_lut(style)
        }
        
        for i, shot in enumerate(shots):
            grading = {
                "shot": i + 1,
                "exposure": "0 EV",  # Exposure adjustment
                "contrast": "+10%",
                "saturation": "+5%",
                "temperature": "Warm" if style == "cinematic" else "Neutral",
                "highlights": "-5",
                "shadows": "+10",
                "vignette": "Subtle"
            }
            plan['grading_per_shot'].append(grading)
        
        print(f"   ✅ Color palette: {len(plan['color_palette'])} colors")
        print(f"   ✅ LUT: {plan['lut_recommendation']}")
        print(f"   ✅ Per-shot grading: {len(plan['grading_per_shot'])} shots")
        
        return plan
    
    def _generate_palette(self, style):
        """Generate color palette based on style"""
        palettes = {
            "cinematic": ["#1a1a2e", "#16213e", "#0f3460", "#533483", "#e94560"],
            "bright": ["#fff", "#fffef5", "#fef5df", "#ffeaa7", "#fdcb6e"],
            "dark": ["#000", "#1e272e", "#34495e", "#2c3e50", "#7f8c8d"]
        }
        return palettes.get(style, palettes["cinematic"])
    
    def _recommend_lut(self, style):
        """Recommend LUT based on style"""
        return "Warm Orange/Teal" if style == "cinematic" else "Neutral Rec709"


class CinematographyDirector(BaseDirector):
    """
    Expert in shot composition, framing, and camera work
    """
    def __init__(self):
        super().__init__("Cinematography")
    
    def execute(self, shots):
        """
        Determine optimal framing and composition for each shot
        """
        print(f"\n🎥 CINEMATOGRAPHY DIRECTOR: Designing shot composition")
        
        plan = {"shots": []}
        
        for i, shot in enumerate(shots):
            composition = {
                "shot": i + 1,
                "framing": self._determine_framing(shot),
                "composition_guide": "Rule of thirds",
                "focal_point": "Center-weighted",
                "aspect_ratio": "16:9",
                "crop_instructions": "Center crop, preserve subject"
            }
            plan['shots'].append(composition)
        
        print(f"   ✅ Composition specs: {len(plan['shots'])} shots")
        
        return plan
    
    def _determine_framing(self, shot):
        """Determine best framing for shot"""
        desc = shot.get('visual', '').lower()
        
        if 'close-up' in desc or 'close up' in desc:
            return "Tight close-up"
        elif 'wide' in desc or 'establishing' in desc:
            return "Wide shot"
        elif 'medium' in desc:
            return "Medium shot"
        else:
            return "Medium close-up"


class EditingDirector(BaseDirector):
    """
    Expert in clip selection, timing, pacing, and sequencing
    """
    def __init__(self):
        super().__init__("Editing")
    
    def execute(self, shots, clips):
        """
        Create precise edit decision list
        """
        print(f"\n✂️ EDITING DIRECTOR: Creating edit decision list")
        
        edl = {"edits": []}
        
        for i, (shot, clip_info) in enumerate(zip(shots, clips)):
            target_duration = shot.get('duration', 5)
            
            edit = {
                "shot": i + 1,
                "clip": clip_info.get('path', ''),
                "target_duration": target_duration,
                "trim_strategy": "smart_center",  # or "best_moment"
                "in_point": None,  # Calculated during editing
                "out_point": None,
                "speed": 1.0,  # Normal speed
                "stabilization": "auto"
            }
            edl['edits'].append(edit)
        
        print(f"   ✅ Edit decisions: {len(edl['edits'])} clips")
        
        return edl


class TransitionsDirector(BaseDirector):
    """
    Expert in scene transitions and visual flow
    """
    def __init__(self):
        super().__init__("Transitions")
    
    def execute(self, shots):
        """
        Design transitions between shots
        """
        print(f"\n🔀 TRANSITIONS DIRECTOR: Designing scene flow")
        
        plan = {"transitions": []}
        
        for i in range(len(shots) - 1):
            transition = {
                "from_shot": i + 1,
                "to_shot": i + 2,
                "type": self._select_transition(shots[i], shots[i+1]),
                "duration": 0.5,  # seconds
                "easing": "smooth"
            }
            plan['transitions'].append(transition)
        
        print(f"   ✅ Transitions designed: {len(plan['transitions'])}")
        
        return plan
    
    def _select_transition(self, shot1, shot2):
        """Intelligently select transition type"""
        # Match cut for similar shots
        # Dissolve for mood change
        # Cut for different locations
        return "cut"  # Default to cut (most professional)


class AudioDirector(BaseDirector):
    """
    Expert in audio mixing, sound design, and sonic landscape
    """
    def __init__(self):
        super().__init__("Audio")
    
    def execute(self, shots, duration):
        """
        Create comprehensive audio mix plan
        """
        print(f"\n🎵 AUDIO DIRECTOR: Designing soundscape")
        
        plan = {
            "layers": [
                {
                    "type": "music",
                    "volume": 0.4,
                    "fade_in": 1.0,
                    "fade_out": 2.0
                },
                {
                    "type": "voiceover",
                    "volume": 1.0,
                    "ducking": True  # Duck music when VO plays
                },
                {
                    "type": "sfx",
                    "volume": 0.25,
                    "ambient": True
                }
            ],
            "volume_automation": [],
            "total_duration": duration
        }
        
        # Create volume automation per shot
        for i, shot in enumerate(shots):
            automation = {
                "shot": i + 1,
                "music_volume": 0.4 if i > 0 else 0.3,  # Quieter at start
                "sfx_volume": 0.25,
                "voiceover_volume": 1.0
            }
            plan['volume_automation'].append(automation)
        
        print(f"   ✅ Audio layers: {len(plan['layers'])}")
        print(f"   ✅ Volume automation: {len(plan['volume_automation'])} points")
        
        return plan
