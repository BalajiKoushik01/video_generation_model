import os
import requests
from config import ASSETS_DIR

class PixabayAgent:
    """
    Pixabay API - 2.7 million+ royalty-free images and videos.
    Serves as backup for Pexels.
    """
    def __init__(self):
        self.api_key = "demo"  # Free key available at pixabay.com/api/docs/
        self.base_url = "https://pixabay.com/api"
        
    def search_video(self, query):
        """
        Searches for HD/4K videos.
        Returns path to downloaded video.
        """
        print(f"   🎥 Searching Pixabay for: '{query}'...")
        
        url = f"{self.base_url}/videos/"
        params = {
            "key": self.api_key,
            "q": query,
            "per_page": 5,
            "video_type": "all"
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('hits'):
                    # Get highest quality video
                    video = data['hits'][0]
                    videos = video.get('videos', {})
                    
                    # Try to get highest quality
                    download_url = None
                    for quality in ['large', 'medium', 'small']:
                        if quality in videos:
                            download_url = videos[quality]['url']
                            break
                    
                    if download_url:
                        filename = f"pixabay_{query.replace(' ', '_')}_{video['id']}.mp4"
                        if not os.path.exists(ASSETS_DIR):
                            os.makedirs(ASSETS_DIR)
                        save_path = os.path.join(ASSETS_DIR, filename)
                        
                        if not os.path.exists(save_path):
                            print(f"   ⬇️ Downloading video from Pixabay...")
                            vid_response = requests.get(download_url, stream=True)
                            with open(save_path, 'wb') as f:
                                for chunk in vid_response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            print(f"   ✅ Video acquired from Pixabay")
                            return save_path
                        else:
                            return save_path
                else:
                    print(f"   ⚠️ No videos found on Pixabay")
                    return None
            else:
                print(f"   ⚠️ Pixabay API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Pixabay Error: {e}")
            return None
    
    def search_image(self, query):
        """
        Searches for high-quality images.
        """
        url = f"{self.base_url}/"
        params = {
            "key": self.api_key,
            "q": query,
            "image_type": "photo",
            "per_page": 5
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('hits'):
                    image = data['hits'][0]
                    download_url = image['largeImageURL']
                    
                    filename = f"pixabay_{query.replace(' ', '_')}_{image['id']}.jpg"
                    if not os.path.exists(ASSETS_DIR):
                        os.makedirs(ASSETS_DIR)
                    save_path = os.path.join(ASSETS_DIR, filename)
                    
                    if not os.path.exists(save_path):
                        img_response = requests.get(download_url)
                        with open(save_path, 'wb') as f:
                            f.write(img_response.content)
                        return save_path
                    else:
                        return save_path
                        
        except Exception as e:
            print(f"   ❌ Pixabay Image Error: {e}")
            return None
