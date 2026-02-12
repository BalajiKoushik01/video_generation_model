"""
Enhanced Sound Department - Using Freesound API + Royalty-Free Music
Simple, reliable audio sourcing without AI generation
"""
import os
import requests
from config import OUTPUT_DIR, FREESOUND_API_KEY

class SoundDeptAgent:
    """
    Sources professional background music and ambient sounds.
    Uses Freesound API for royalty-free audio content.
    """
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.api_key = FREESOUND_API_KEY
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_music(self, mood="cinematic", duration=30, style="background"):
        """
        Source professional background music from Freesound.
        
        Args:
            mood: Musical mood (cinematic, upbeat, calm, etc.)
            duration: Desired length in seconds
            style: Music style
        
        Returns:
            Path to downloaded music file
        """
        print(f"   🎵 Sourcing {mood} music from Freesound...")
        
        if not self.api_key:
            print("   ⚠️ Freesound API key not configured - skipping music")
            return None
        
        try:
            # Search for music matching mood
            search_query = f"{mood} {style} music instrumental"
            
            # Freesound API search
            search_url = "https://freesound.org/apiv2/search/text/"
            params = {
                "query": search_query,
                "filter": f"duration:[{duration-5} TO {duration+10}]",  # Duration range
                "sort": "rating_desc",  # Best quality first
                "fields": "id,name,previews,duration",
                "page_size": 5
            }
            headers = {"Authorization": f"Token {self.api_key}"}
            
            print(f"   🔍 Searching: '{search_query}'...")
            response = requests.get(search_url, params=params, headers=headers, verify=False)
            
            if response.status_code == 200:
                results = response.json()
                
                if results['count'] > 0:
                    # Get first result
                    sound = results['results'][0]
                    sound_id = sound['id']
                    sound_name = sound['name']
                    
                    print(f"   📥 Downloading: {sound_name}")
                    
                    # Get download URL
                    download_url = f"https://freesound.org/apiv2/sounds/{sound_id}/download/"
                    download_response = requests.get(download_url, headers=headers, verify=False)
                    
                    if download_response.status_code == 200:
                        # Save file
                        output_path = os.path.join(self.output_dir, f"background_music.mp3")
                        
                        with open(output_path, 'wb') as f:
                            f.write(download_response.content)
                        
                        print(f"   ✅ Music downloaded: {os.path.basename(output_path)}")
                        return output_path
                    else:
                        print(f"   ⚠️ Download failed: {download_response.status_code}")
                else:
                    print("   ⚠️ No music found matching criteria")
            else:
                print(f"   ⚠️ Freesound API error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Music sourcing failed: {e}")
            
        # FALLBACK: Use local music if API failed
        fallback_path = os.path.join(self.output_dir, "..", "assets", "fallback_music.mp3")
        if os.path.exists(fallback_path):
            print(f"   🎵 Using fallback library music: {os.path.basename(fallback_path)}")
            return fallback_path
        else:
            print("   ⚠️ No fallback music found in assets/")
            return None
    
    def generate_ambient_sound(self, scene_type="coffee shop"):
        """
        Source ambient sound for specific scene types.
        
        Args:
            scene_type: Type of scene (coffee shop, city, nature, etc.)
        
        Returns:
            Path to downloaded ambient audio
        """
        print(f"   🔊 Sourcing ambient sound: {scene_type}...")
        
        if not self.api_key:
            print("   ⚠️ Freesound API key not configured")
            return None
        
        try:
            search_url = "https://freesound.org/apiv2/search/text/"
            params = {
                "query": f"{scene_type} ambience ambient",
                "filter": "duration:[5 TO 30]",
                "sort": "rating_desc",
                "fields": "id,name,previews",
                "page_size": 3
            }
            headers = {"Authorization": f"Token {self.api_key}"}
            
            response = requests.get(search_url, params=params, headers=headers, verify=False)
            
            if response.status_code == 200:
                results = response.json()
                
                if results['count'] > 0:
                    sound = results['results'][0]
                    sound_id = sound['id']
                    
                    download_url = f"https://freesound.org/apiv2/sounds/{sound_id}/download/"
                    download_response = requests.get(download_url, headers=headers, verify=False)
                    
                    if download_response.status_code == 200:
                        output_path = os.path.join(self.output_dir, f"ambient_{scene_type.replace(' ', '_')}.mp3")
                        
                        with open(output_path, 'wb') as f:
                            f.write(download_response.content)
                        
                        print(f"   ✅ Ambient sound downloaded")
                        return output_path
            
        except Exception as e:
            print(f"   ⚠️ Ambient sourcing failed: {e}")
        
        return None
    
    def compose_score(self, prompt, duration=30):
        """
        Alias for generate_music - composes background score.
        Called by studio.py during production.
        """
        return self.generate_music(mood="cinematic", duration=duration, style="background")
