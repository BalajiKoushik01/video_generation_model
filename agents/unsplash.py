import os
import requests
from config import ASSETS_DIR

class UnsplashAgent:
    """
    Unsplash API - 3 million+ high-resolution photos.
    No API key required for basic use (demo mode).
    """
    def __init__(self):
        self.base_url = "https://api.unsplash.com"
        # Using demo client ID (limited to 50 requests/hour)
        # Users can get free key at unsplash.com/developers
        self.client_id = "demo"  # Replace with actual key for production
        
    def search_photo(self, query, orientation="landscape"):
        """
        Searches for high-quality photos.
        Returns path to downloaded image.
        """
        print(f"   📸 Searching Unsplash for: '{query}'...")
        
        url = f"{self.base_url}/search/photos"
        params = {
            "query": query,
            "per_page": 5,
            "orientation": orientation,
            "order_by": "relevant"
        }
        
        # For demo mode, use source.unsplash.com (no auth required)
        try:
            # Fallback to direct image URL (no API key needed)
            # This uses Unsplash Source API
            direct_url = f"https://source.unsplash.com/1920x1080/?{query.replace(' ', ',')}"
            
            filename = f"unsplash_{query.replace(' ', '_')}.jpg"
            if not os.path.exists(ASSETS_DIR):
                os.makedirs(ASSETS_DIR)
            save_path = os.path.join(ASSETS_DIR, filename)
            
            if not os.path.exists(save_path):
                print(f"   ⬇️ Downloading high-res photo...")
                response = requests.get(direct_url, stream=True)
                if response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"   ✅ Photo acquired from Unsplash")
                    return save_path
                else:
                    print(f"   ⚠️ Unsplash Error: {response.status_code}")
                    return None
            else:
                print(f"   ✅ Using cached photo")
                return save_path
                
        except Exception as e:
            print(f"   ❌ Unsplash Error: {e}")
            return None
    
    def get_random_photo(self, category="nature"):
        """
        Gets a random high-quality photo from a category.
        """
        categories = {
            "nature": "nature,landscape",
            "city": "city,urban",
            "business": "business,office",
            "food": "food,culinary",
            "technology": "technology,modern"
        }
        
        query = categories.get(category.lower(), category)
        return self.search_photo(query)
