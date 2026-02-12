import os
import requests
from config import OUTPUT_DIR

class SoundEffectsAgent:
    """
    Uses Freesound API to add professional sound effects to videos.
    Freesound has 500,000+ royalty-free sounds.
    """
    def __init__(self):
        # Freesound doesn't require API key for basic searches
        self.base_url = "https://freesound.org/apiv2"
        
    def find_sound_effect(self, query, duration=None):
        """
        Searches for sound effects matching the query.
        Returns path to downloaded sound file.
        """
        print(f"   🔊 Searching for sound effect: '{query}'...")
        
        # Use text search endpoint (no auth required for search)
        url = f"{self.base_url}/search/text/"
        params = {
            "query": query,
            "filter": "duration:[0 TO 10]",  # Short sounds only
            "sort": "rating_desc",
            "fields": "id,name,previews,duration"
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('results'):
                    # Get the highest-rated sound
                    sound = data['results'][0]
                    preview_url = sound['previews']['preview-hq-mp3']
                    
                    # Download it
                    filename = f"sfx_{query.replace(' ', '_')}_{sound['id']}.mp3"
                    save_path = os.path.join(OUTPUT_DIR, filename)
                    
                    if not os.path.exists(save_path):
                        print(f"   ⬇️ Downloading sound effect...")
                        audio_response = requests.get(preview_url)
                        with open(save_path, 'wb') as f:
                            f.write(audio_response.content)
                    
                    print(f"   ✅ Sound effect acquired: {sound['name']}")
                    return save_path
                else:
                    print(f"   ⚠️ No sound effects found for '{query}'")
                    return None
            else:
                print(f"   ⚠️ Freesound API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Sound Effects Error: {e}")
            return None
    
    def get_ambient_sound(self, scene_type):
        """
        Gets appropriate ambient sound based on scene type.
        """
        ambient_map = {
            "coffee shop": "coffee shop ambience",
            "city": "city traffic",
            "nature": "forest birds",
            "office": "office ambience",
            "kitchen": "kitchen sounds",
            "car": "car interior"
        }
        
        query = ambient_map.get(scene_type.lower(), "ambient background")
        return self.find_sound_effect(query)
