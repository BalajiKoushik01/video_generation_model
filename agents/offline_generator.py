"""
Offline Asset Generator - Creates placeholder assets when network is unavailable
Uses Pillow for image generation and MoviePy for video creation
"""
import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip
from config import ASSETS_DIR, OUTPUT_DIR
import random

class OfflineGenerator:
    """
    Generates high-quality placeholder assets offline when APIs are unavailable.
    """
    def __init__(self):
        if not os.path.exists(ASSETS_DIR):
            os.makedirs(ASSETS_DIR)
        self.colors = {
            "coffee": [(101, 67, 33), (139, 69, 19), (160, 82, 45)],  # Browns
            "tech": [(41, 128, 185), (52, 73, 94), (149, 165, 166)],  # Blues/Grays
            "nature": [(39, 174, 96), (46, 204, 113), (22, 160, 133)],  # Greens
            "luxury": [(192, 57, 43), (231, 76, 60), (52, 73, 94)]  # Reds/Dark
        }
    
    def generate_image(self, query, width=1920, height=1080):
        """
        Generate a styled placeholder image based on query.
        Better than generic placeholders - uses theme-based gradients.
        """
        print(f"   🎨 Generating offline placeholder for: '{query}'")
        
        # Detect theme
        theme = self._detect_theme(query)
        colors = self.colors.get(theme, self.colors["tech"])
        
        # Create gradient background
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Gradient effect
        for y in range(height):
            ratio = y / height
            color = self._interpolate_color(colors[0], colors[1], ratio)
            draw.line([(0, y), (width, y)], fill=color)
        
        # Add overlay pattern
        self._add_pattern(draw, width, height, colors[2])
        
        # Add text
        try:
            # Try to use a nice font
            font = ImageFont.truetype("arial.ttf", 80)
        except:
            font = ImageFont.load_default()
        
        # Clean query for display
        display_text = query.upper()[:30]
        bbox = draw.textbbox((0, 0), display_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Shadow
        draw.text((position[0]+3, position[1]+3), display_text, fill=(0,0,0,128), font=font)
        # Main text
        draw.text(position, display_text, fill=(255,255,255), font=font)
        
        # Save
        filename = f"offline_{query.replace(' ', '_')}_{random.randint(1000,9999)}.jpg"
        filepath = os.path.join(ASSETS_DIR, filename)
        img.save(filepath, quality=95)
        
        print(f"   ✅ Generated: {filename}")
        return filepath
    
    def generate_video(self, query, duration=5, width=1920, height=1080):
        """
        Generate a video placeholder with motion effect.
        """
        print(f"   🎬 Creating offline video for: '{query}'")
        
        # Generate base image
        img_path = self.generate_image(query, width, height)
        
        # Create video clip with zoom effect
        clip = ImageClip(img_path, duration=duration)
        
        # Add subtle zoom
        clip = clip.resize(lambda t: 1 + 0.05 * t / duration)
        
        # Save as video
        filename = f"offline_{query.replace(' ', '_')}_{random.randint(1000,9999)}.mp4"
        filepath = os.path.join(ASSETS_DIR, filename)
        
        clip.write_videofile(filepath, fps=24, codec='libx264', audio=False,
                            logger=None, verbose=False)
        
        print(f"   ✅ Generated video: {filename}")
        return filepath
    
    def _detect_theme(self, query):
        """Detect theme from query for appropriate colors."""
        q = query.lower()
        if any(w in q for w in ['coffee', 'cafe', 'espresso', 'latte']):
            return 'coffee'
        elif any(w in q for w in ['tech', 'digital', 'computer', 'phone']):
            return 'tech'
        elif any(w in q for w in ['nature', 'forest', 'tree', 'mountain']):
            return 'nature'
        elif any(w in q for w in ['luxury', 'premium', 'gold', 'watch']):
            return 'luxury'
        return 'tech'
    
    def _interpolate_color(self, color1, color2, ratio):
        """Interpolate between two RGB colors."""
        return tuple(int(c1 + (c2 - c1) * ratio) for c1, c2 in zip(color1, color2))
    
    def _add_pattern(self, draw, width, height, color):
        """Add subtle pattern overlay."""
        # Diagonal lines pattern
        for i in range(0, width + height, 100):
            draw.line([(i, 0), (0, i)], fill=color, width=2)
