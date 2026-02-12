import os
import requests
import random
from config import PEXELS_API_KEY, ASSETS_DIR

class LibrarianAgent:
    def __init__(self):
        self.api_key = PEXELS_API_KEY
        self.headers = {"Authorization": self.api_key}
        
    def find_stock_footage(self, query):
        """
        Searches Pexels for 4K video matching the query.
        Returns the local path of the downloaded file.
        """
        print(f"   🔎 Searching Pexels for: '{query}'...")
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=5&orientation=landscape&size=medium" # size=medium for speed, use 'large' for 4K
        
        response = requests.get(url, headers=self.headers, verify=False, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('videos'):
                # Pick the best quality video file from the first result
                video_files = data['videos'][0]['video_files']
                # Sort by resolution (width) descending to get best quality
                best_video = sorted(video_files, key=lambda x: x['width'], reverse=True)[0]
                download_url = best_video['link']
                
                # Download it
                safe_query = "".join([c for c in query if c.isalpha() or c.isdigit() or c==' ']).strip().replace(' ', '_')
                filename = f"{safe_query}_{data['videos'][0]['id']}.mp4"
                if not os.path.exists(ASSETS_DIR): os.makedirs(ASSETS_DIR)
                save_path = os.path.join(ASSETS_DIR, filename)
                
                if not os.path.exists(save_path):
                    print(f"   ⬇️ Downloading stock footage...")
                    try:
                        with requests.get(download_url, stream=True, verify=False, timeout=30) as r:
                            r.raise_for_status()
                            with open(save_path, 'wb') as f:
                                for chunk in r.iter_content(chunk_size=8192):
                                    f.write(chunk)
                    except Exception as e:
                        print(f"      ❌ Download Error: {e}")
                        return None
                return save_path
            else:
                print(f"   ⚠️ Pexels returned no videos for '{query}'.")
                return None
        else:
            print(f"   ❌ Pexels API Error {response.status_code}: {response.text}")
            return None
