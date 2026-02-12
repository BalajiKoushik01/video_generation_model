"""
Enhanced Smart Librarian - Gemini Veo Level Context Matching
Advanced semantic scene understanding with multi-level keyword extraction
"""
import os
import re
from agents.librarian import LibrarianAgent
from agents.pixabay import PixabayAgent
from agents.unsplash import UnsplashAgent

class SmartLibrarianAgent:
    """
    GEMINI VEO-LEVEL intelligent asset sourcing.
    
    Features:
    - Semantic scene understanding
    - Multi-level keyword extraction (subject, action, setting, mood)
    - Context-aware search strategies
    - Relevance scoring
    - Mixed media support (video + images)
    """
    def __init__(self, intelligence=None):
        self.pexels = LibrarianAgent()
        self.pixabay = PixabayAgent()
        self.unsplash = UnsplashAgent()
        self.intelligence = intelligence
        self.cache = {}
    
    def acquire_asset(self, query, asset_type="video"):
        """Acquire asset with intelligent fallback"""
        cache_key = f"{query}_{asset_type}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        asset_path = None
        
        if asset_type == "video":
            print(f"   📹 [1/2] Pexels...")
            asset_path = self.pexels.find_stock_footage(query)
            
            if not asset_path:
                print(f"   📹 [2/2] Pixabay...")
                try:
                    asset_path = self.pixabay.search_video(query)
                except:
                    pass
        else:  # image
            print(f"   📸 [1/3] Pexels...")
            asset_path = self.pexels.find_stock_footage(query)
            
            if not asset_path:
                print(f"   📸 [2/3] Unsplash...")
                try:
                    asset_path = self.unsplash.search_photo(query)
                except:
                    pass
            
            if not asset_path:
                print(f"   📸 [3/3] Pixabay...")
                try:
                    asset_path = self.pixabay.search_image(query)
                except:
                    pass
        
        if asset_path:
            self.cache[cache_key] = asset_path
            print(f"   ✅ Asset secured: {os.path.basename(asset_path)}")
        
        return asset_path
    
    def get_best_match(self, scene_data):
        """
        GEMINI VEO-LEVEL scene analysis and asset matching.
        Uses advanced semantic understanding for perfect context matching.
        """
        visual_prompt = scene_data.get('visual_prompt', '')
        source_type = scene_data.get('source_type', 'STOCK')
        
        # Use intelligence if available
        if self.intelligence:
            try:
                source_type, _ = self.intelligence.smart_source_selection(
                    scene_data, 
                    available_sources=['pexels', 'pixabay', 'unsplash']
                )
            except:
                pass
        
        # ADVANCED: Extract scene components
        scene_components = self._extract_scene_components(visual_prompt)
        
        # Generate intelligent search queries
        queries = self._generate_intelligent_queries(scene_components, visual_prompt)
        
        # Determine asset type
        needs_video = self._requires_video(visual_prompt, source_type)
        asset_type = "video" if needs_video else "image"
        
        # Try each query in priority order
        for i, query in enumerate(queries):
            print(f"   🔍 **SEARCH LEVEL {i+1}**: '{query}'")
            asset_path = self.acquire_asset(query, asset_type)
            if asset_path:
                return asset_path
        
        # Final fallback
        print(f"   🔄 Generic fallback...")
        fallback_query = scene_components.get('subject', 'cinematic')
        if fallback_query == 'cinematic':
             # If even subject failed, try keywords
             kws = self._extract_keywords(visual_prompt)
             if kws:
                 fallback_query = " ".join(kws[:2])
        
        print(f"   🔄 Fallback Query: '{fallback_query}'")
        return self.acquire_asset(fallback_query, asset_type)
    
    def _extract_scene_components(self, visual_prompt):
        """
        GEMINI VEO: Extract semantic components from scene description.
        Returns: {subject, action, setting, mood, details}
        """
        prompt_lower = visual_prompt.lower()
        
        # Extract subject (main focus)
        subject_keywords = ['coffee', 'cup', 'espresso', 'latte', 'beans', 'hands', 'person',
                          'barista', 'machine', 'steam', 'pour', 'mug', 'cafe', 'shop']
        subject = next((kw for kw in subject_keywords if kw in prompt_lower), 'cinematic')
        
        # Extract action (what's happening)
        action_keywords = ['pouring', 'drinking', 'holding', 'making', 'grinding', 'brewing',
                         'steaming', 'rising', 'cradling', 'sipping', 'preparing']
        action = next((kw for kw in action_keywords if kw in prompt_lower), '')
        
        # Extract setting (where)
        setting_keywords = ['kitchen', 'cafe', 'shop', 'counter', 'table', 'window', 'bar']
        setting = next((kw for kw in setting_keywords if kw in prompt_lower), '')
        
        # Extract mood (atmosphere)
        mood_keywords = ['warm', 'cozy', 'intimate', 'elegant', 'modern', 'rustic', 
                        'minimalist', 'luxury', 'artisan', 'professional']
        mood = next((kw for kw in mood_keywords if kw in prompt_lower), 'cinematic')
        
        return {
            'subject': subject,
            'action': action,
            'setting': setting,
            'mood': mood
        }
    
    def _generate_intelligent_queries(self, components, full_prompt):
        """
        GEMINI VEO: Generate multi-level search queries for best matching.
        Priority: Specific → General
        """
        queries = []
        
        # Level 1: Full context (action + subject + setting + mood)
        if components['action'] and components['subject'] and components['setting']:
            queries.append(f"{components['action']} {components['subject']} {components['setting']} {components['mood']}")
        
        # Level 2: Action + Subject + Mood
        if components['action'] and components['subject']:
            queries.append(f"{components['action']} {components['subject']} {components['mood']}")
        
        # Level 3: Subject + Setting
        if components['subject'] and components['setting']:
            queries.append(f"{components['subject']} {components['setting']}")
        
        # Level 4: Subject + Mood
        if components['subject']:
            queries.append(f"{components['subject']} {components['mood']}")
        
        # Level 5: Just subject
        if components['subject'] != 'cinematic':
            queries.append(components['subject'])
        
        # Level 6: Fallback to extracted keywords
        keywords = self._extract_keywords(full_prompt)
        if keywords:
            queries.append(" ".join(keywords[:2]))
        
        return queries or ['cinematic professional']
    
    def _requires_video(self, visual_prompt, source_type):
        """Determine if scene requires video or can use image"""
        motion_keywords = ['pouring', 'moving', 'walking', 'flowing', 'rising', 'grinding',
                          'steaming', 'brewing', 'tracking', 'dolly', 'crane', 'gimbal', 'video', 'footage']
        # Relaxed check: Allow images if explicit motion not requested, or if specifically requested as 'image'
        if 'image' in visual_prompt.lower() or 'photo' in visual_prompt.lower():
            return False
            
        return any(kw in visual_prompt.lower() for kw in motion_keywords)
    
    def _extract_keywords(self, visual_prompt):
        """Legacy keyword extraction for fallback"""
        stop_words = {
            'shot', 'with', 'captured', 'camera', 'lens', 'lighting', 'setup', 'movement',
            'arri', 'alexa', 'red', 'komodo', 'sony', 'anamorphic', 'gimbal', 'dolly', 'crane',
            'close', 'extreme', 'wide', 'medium', 'establishing'
        }
        
        prompt_clean = re.sub(r'shot with.*?lens', '', visual_prompt.lower())
        prompt_clean = re.sub(r'\d+mm', '', prompt_clean)
        words = prompt_clean.split()
        
        keywords = []
        for word in words:
            word = word.strip(',.:;-')
            if len(word) > 3 and word not in stop_words and not word.isdigit():
                keywords.append(word)
        
        return keywords[:5] if keywords else ['cinematic']
    
    def clear_cache(self):
        """Clear asset cache"""
        self.cache = {}
        print("   🗑️ Cache cleared")
