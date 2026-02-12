import requests
import json

class ColorGradingAgent:
    """
    Uses Colormind AI API to generate professional color palettes
    for video color grading and brand consistency.
    """
    def __init__(self):
        self.api_url = "http://colormind.io/api/"
        
    def generate_palette(self, mood="cinematic"):
        """
        Generates a 5-color palette based on mood.
        Returns RGB values for color grading.
        """
        print(f"   🎨 Generating {mood} color palette...")
        
        # Colormind models
        models = {
            "cinematic": "default",  # Balanced, professional
            "vibrant": "default",
            "moody": "default",
            "warm": "default",
            "cool": "default"
        }
        
        model = models.get(mood.lower(), "default")
        
        payload = {
            "model": model
        }
        
        try:
            response = requests.post(self.api_url, json=payload, verify=False, timeout=10)
            if response.status_code == 200:
                data = response.json()
                palette = data['result']
                
                print(f"   ✅ Color Palette Generated:")
                for i, color in enumerate(palette):
                    rgb = f"RGB({color[0]}, {color[1]}, {color[2]})"
                    hex_color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
                    print(f"      Color {i+1}: {hex_color} - {rgb}")
                
                return {
                    "palette": palette,
                    "hex": ["#{:02x}{:02x}{:02x}".format(c[0], c[1], c[2]) for c in palette],
                    "mood": mood
                }
            else:
                print(f"   ⚠️ Colormind API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Color Grading Error: {e}")
            return None
    
    def get_brand_palette(self, primary_color_hex=None):
        """
        Generates a complementary palette based on a brand color.
        """
        if primary_color_hex:
            # Convert hex to RGB
            hex_color = primary_color_hex.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            payload = {
                "model": "default",
                "input": [[rgb[0], rgb[1], rgb[2]], "N", "N", "N", "N"]
            }
            
            try:
                response = requests.post(self.api_url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    return data['result']
            except:
                pass
        
        return self.generate_palette()
    
    def suggest_lut(self, palette):
        """
        Suggests LUT (Look-Up Table) settings based on palette.
        """
        if not palette:
            return None
            
        # Analyze palette warmth/coolness
        avg_red = sum(c[0] for c in palette['palette']) / 5
        avg_blue = sum(c[2] for c in palette['palette']) / 5
        
        if avg_red > avg_blue + 20:
            return "Warm (Orange/Teal)"
        elif avg_blue > avg_red + 20:
            return "Cool (Teal/Blue)"
        else:
            return "Neutral (Balanced)"
