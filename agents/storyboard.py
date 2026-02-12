import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from config import OUTPUT_DIR

class StoryboardAgent:
    def __init__(self):
        print("   🎨 Initializing Storyboard Agent...")
    
    def create_storyboard(self, script, visuals_map):
        """
        Creates a PDF storyboard from the script and generated visual assets (or placeholders).
        visuals_map: dict mapping scene_index to image_path
        """
        print("   📋 Creating Production Storyboard...")
        
        pdf_path = os.path.join(OUTPUT_DIR, "Storyboard.pdf")
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        
        # Title Page
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width/2, height-100, "HOLLYWOOD STUDIO")
        c.setFont("Helvetica", 18)
        c.drawCentredString(width/2, height-140, "Production Storyboard")
        c.setFont("Helvetica-Oblique", 12)
        c.drawCentredString(width/2, height-170, f"Generated: {script.get('vision', 'Untitled Project')}")
        c.showPage()
        
        # Scenes (3 per page)
        y_pos = height - 50
        scenes = script.get('scenes', [])
        if not scenes and 'shots' in script:
            scenes = script['shots'] # Handle Super Director format
            
        for i, scene in enumerate(scenes):
            if y_pos < 250:
                c.showPage()
                y_pos = height - 50
                
            # Scene Header
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_pos, f"SCENE {i+1}: {scene.get('visual', scene.get('visual_prompt', ''))[:60]}...")
            y_pos -= 20
            
            # Image (if available)
            img_path = visuals_map.get(i)
            if img_path and os.path.exists(img_path):
                try:
                    # Draw Image (Aspect Ratio 16:9 approx)
                    img_w = 400
                    img_h = 225
                    c.drawImage(img_path, 100, y_pos - img_h, width=img_w, height=img_h)
                    y_pos -= (img_h + 20)
                except:
                    c.drawString(100, y_pos - 100, "[Image Error]")
                    y_pos -= 120
            else:
                # Placeholder box
                c.rect(100, y_pos - 150, 400, 150)
                c.drawString(250, y_pos - 75, "[Visual Placeholder]")
                y_pos -= 170
                
            # Details
            c.setFont("Helvetica", 10)
            c.drawString(50, y_pos, f"Action: {scene.get('motion_prompt', scene.get('technical', ''))[:80]}")
            y_pos -= 15
            c.drawString(50, y_pos, f"Audio: {scene.get('audio_needs', scene.get('voiceover', ''))[:80]}")
            y_pos -= 40 # Spacer
            
        c.save()
        print(f"   ✅ Storyboard saved: {pdf_path}")
        return pdf_path
