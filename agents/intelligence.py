"""
Intelligence Layer - Makes the entire system adaptive and self-optimizing
"""
import os
import json
import time
import requests
from datetime import datetime

class IntelligenceAgent:
    """
    Central intelligence that makes the studio adaptive and self-improving.
    """
    def __init__(self):
        self.knowledge_base = self._load_knowledge()
        self.network_status = self._detect_network()
        
    def _load_knowledge(self):
        """Load learned patterns and preferences."""
        kb_path = "C:\\Users\\balaj\\Desktop\\AI\\Hollywood_Studio\\knowledge.json"
        if os.path.exists(kb_path):
            with open(kb_path, 'r') as f:
                return json.load(f)
        return {
            "successful_prompts": [],
            "failed_prompts": [],
            "best_sources": {"video": "pexels", "image": "pexels"},
            "avg_scene_count": 5,
            "preferred_duration": 25,
            "quality_threshold": 0.7
        }
    
    def _detect_network(self):
        """Intelligently detect network conditions and proxy."""
        print("🧠 Intelligence: Analyzing network environment...")
        
        status = {
            "has_internet": False,
            "needs_proxy": False,
            "firewall_detected": False,
            "api_access": {},
            "recommended_mode": "offline"
        }
        
        # Test APIs with smart timeout
        apis = {
            "groq": "https://api.groq.com",
            "pexels": "https://api.pexels.com",
            "google": "https://www.google.com"
        }
        
        for name, url in apis.items():
            try:
                response = requests.get(url, timeout=3, verify=False)
                if response.status_code < 500:
                    status["api_access"][name] = True
                    status["has_internet"] = True
                else:
                    status["api_access"][name] = False
            except requests.exceptions.SSLError:
                status["firewall_detected"] = True
                status["api_access"][name] = False
            except:
                status["api_access"][name] = False
        
        # Determine mode
        if sum(status["api_access"].values()) >= 2:
            status["recommended_mode"] = "full"
        elif sum(status["api_access"].values()) == 1:
            status["recommended_mode"] = "hybrid"
        else:
            status["recommended_mode"] = "offline"
            
        print(f"   🌐 Network Mode: {status['recommended_mode'].upper()}")
        print(f"   📡 API Access: {sum(status['api_access'].values())}/3")
        
        return status
    
    def assess_script_quality(self, script):
        """Assess script quality and provide feedback""" 
        if not script:
            return {'score': 0, 'grade': 'F', 'issues': ['No script'], 'recommendations': []}
        
        scenes = script.get('scenes', [])
        
        # Handle both old and new script formats
        if scenes and isinstance(scenes[0], str):
            # Old format - just a list of strings
            scene_count = len(scenes)
            total_duration = 15  # Default estimate
        else:
            # New format - list of dicts
            scene_count = len(scenes)
            total_duration = sum(s.get('duration', 0) for s in scenes if isinstance(s, dict))
        
        score = 0.0
        issues = []
        recommendations = []
        
        # Check 1: Scene count (5-7 is optimal)
        if 5 <= scene_count <= 7:
            score += 0.2
        elif scene_count < 3:
            issues.append("Too few scenes (< 3)")
            recommendations.append("Add more variety")
        
        # Check 2: Duration (25-30s is optimal)
        total_duration = sum(s.get('duration', 0) for s in scenes)
        if 25 <= total_duration <= 30:
            score += 0.2
        elif total_duration < 15:
            issues.append("Too short (< 15s)")
        
        # Check 3: Stock vs Generate balance
        stock_count = sum(1 for s in scenes if s.get('source_type') == 'STOCK')
        if stock_count >= len(scenes) * 0.7:  # 70%+ stock is good
            score += 0.2
        else:
            recommendations.append("Use more STOCK footage for reliability")
        
        # Check 4: Voiceover presence
        has_vo = any(s.get('voiceover') for s in scenes)
        if has_vo:
            score += 0.2
        else:
            recommendations.append("Add voiceover text for narration")
        
        # Check 5: Visual diversity
        prompts = [s.get('visual_prompt', '') for s in scenes]
        unique_words = set()
        for p in prompts:
            unique_words.update(p.lower().split()[:10])
        if len(unique_words) > 20:  # Good variety
            score += 0.2
        
        return {
            "score": score,
            "grade": self._score_to_grade(score),
            "issues": issues,
            "recommendations": recommendations,
            "passed": score >= self.knowledge_base["quality_threshold"]
        }
    
    def _score_to_grade(self, score):
        """Convert score to letter grade."""
        if score >= 0.9: return "A+"
        if score >= 0.8: return "A"
        if score >= 0.7: return "B"
        if score >= 0.6: return "C"
        return "F"
    
    def smart_source_selection(self, scene, available_sources):
        """
        Intelligently decide which source to use for a scene.
        """
        visual = scene.get('visual_prompt', '').lower()
        source_type = scene.get('source_type', 'STOCK')
        
        # Rule 1: If network is bad, always use STOCK
        if self.network_status["recommended_mode"] == "offline":
            return "STOCK", "local"
        
        # Rule 2: Brand-specific = GENERATE
        brand_keywords = ['logo', 'brand', 'specific product', 'custom']
        if any(kw in visual for kw in brand_keywords):
            return "GENERATE", "ai"
        
        # Rule 3: Generic scenes = STOCK (faster, more reliable)
        stock_keywords = ['coffee', 'person', 'city', 'nature', 'cup', 'pouring']
        if any(kw in visual for kw in stock_keywords):
            return "STOCK", self.knowledge_base["best_sources"]["video"]
        
        # Rule 4: Follow script suggestion
        return source_type, "auto"
    
    def adaptive_retry(self, func, max_attempts=3):
        """
        Smart retry with exponential backoff.
        """
        for attempt in range(max_attempts):
            try:
                result = func()
                if result:
                    return result
            except Exception as e:
                if attempt < max_attempts - 1:
                    wait_time = (2 ** attempt)  # 1s, 2s, 4s
                    print(f"   ⏳ Retry in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"   ❌ Failed after {max_attempts} attempts")
        return None
    
    def learn_from_generation(self, prompt, script, success, assets_count):
        """
        Learn from each generation to improve future results.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "scene_count": len(script.get('scenes', [])),
            "success": success,
            "assets_acquired": assets_count
        }
        
        if success:
            self.knowledge_base["successful_prompts"].append(entry)
            # Update best practices
            if assets_count > 0:
                avg = self.knowledge_base.get("avg_scene_count", 5)
                self.knowledge_base["avg_scene_count"] = (avg + len(script.get('scenes', []))) / 2
        else:
            self.knowledge_base["failed_prompts"].append(entry)
        
        # Save knowledge
        self._save_knowledge()
    
    def _save_knowledge(self):
        """Persist learned knowledge."""
        kb_path = "C:\\Users\\balaj\\Desktop\\AI\\Hollywood_Studio\\knowledge.json"
        with open(kb_path, 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)
    
    def get_smart_recommendations(self, user_prompt):
        """
        Provide intelligent suggestions based on learned patterns.
        """
        recommendations = []
        
        # Based on network
        if self.network_status["recommended_mode"] == "offline":
            recommendations.append("⚠️ Limited network. System will use local/cached assets only.")
        
        # Based on history
        if len(self.knowledge_base["successful_prompts"]) > 0:
            avg_scenes = self.knowledge_base["avg_scene_count"]
            recommendations.append(f"💡 Optimal scene count: {int(avg_scenes)}")
        
        # Based on prompt analysis
        if len(user_prompt.split()) < 3:
            recommendations.append("💡 Add more details to your prompt for better results")
        
        return recommendations
