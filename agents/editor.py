"""
EditorAgent - Professional Video Assembly & Editing
Gemini Veo-Level Post-Production:
- Smart Ken Burns effect for static images
- Professional audio mixing (Music, SFX, Voiceover)
- Seamless transitions
- Robust error handling
"""
import os
import random
from datetime import datetime
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeAudioClip, AudioFileClip, vfx, CompositeVideoClip
from config import OUTPUT_DIR, RESOLUTION, FPS

class EditorAgent:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_filename = f"final_cut_{timestamp}.mp4"
        self.output_path = os.path.join(self.output_dir, self.output_filename)
    
    def assemble_cut(self, assets, audio_path=None, sound_effects=None, voiceover_path=None, production_plan=None, tracker=None):
        """
        Assemble the final video with professional editing techniques.
        """
        print(f"   ✂️ Editor: Starting professional assembly of {len(assets)} assets...")
        
        if not assets:
            print("   ⚠️ No assets to assemble")
            return None
            
        try:
            clips = []
            
            # STEP 1: PROCESSING CLIPS
            for i, asset in enumerate(assets):
                asset_path = asset.get('path')
                target_duration = asset.get('duration', 5)
                
                if not asset_path or not os.path.exists(asset_path):
                    print(f"      ⚠️ Missing asset: {asset_path}")
                    continue
                
                print(f"      🎞️ Processing clip {i+1}: {os.path.basename(asset_path)}")
                
                # CHECK FOR SCENE VOICEOVER
                scene_vo_path = asset.get('voiceover_path')
                if scene_vo_path and os.path.exists(scene_vo_path):
                    try:
                        vo_clip = AudioFileClip(scene_vo_path)
                        # Extend video to match VO if VO is longer
                        if vo_clip.duration > target_duration:
                            print(f"         ⏳ Extending clip duration to {vo_clip.duration:.1f}s to match VO")
                            target_duration = vo_clip.duration
                    except Exception as e:
                        print(f"         ⚠️ Failed to load scene VO: {e}")
                        scene_vo_path = None

                try:
                    clip = None
                    # HANDLE IMAGES (Ken Burns)
                    if asset_path.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        print(f"         🖼️ Applying Ken Burns effect to image...")
                        clip = ImageClip(asset_path).set_duration(target_duration)
                        clip = self._apply_ken_burns(clip, target_duration)
                        
                    # HANDLE VIDEO
                    elif asset_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                        clip = VideoFileClip(asset_path, audio=False) # Strip audio for clean mix
                        
                        # Loop if too short
                        if clip.duration < target_duration:
                             clip = vfx.loop(clip, duration=target_duration)
                        # Trim if too long
                        else:
                            start = (clip.duration - target_duration) / 2
                            clip = clip.subclip(start, start + target_duration)
                    
                    # ATTACH SCENE AUDIO
                    if clip and scene_vo_path:
                        try:
                            # Volumex is applied later in mixing? No, we should apply it here or handle it in mixing.
                            # But wait, step 3 is global mixing.
                            # Better approach: Attach audio to clip, then CompositeAudioClip will include it?
                            # Concatenate_videoclips usually handles audio if present.
                            vo_clip = AudioFileClip(scene_vo_path).volumex(1.5) # Boost VO
                            clip = clip.set_audio(vo_clip)
                            print(f"         ✅ Attached Scene Voiceover")
                        except Exception as e:
                            print(f"         ❌ Failed to attach VO: {e}")
                    
                    if clip:
                        # STANDARDIZE RESOLUTION (1080p)
                        clip = self._resize_to_1080p(clip)
                        
                        # TEXT OVERLAY (Ad Headlines)
                        text = asset.get('text_overlay')
                        if text:
                            clip = self._apply_text_overlay(clip, text, target_duration)
                            
                        clip = clip.set_fps(FPS)
                        clips.append(clip)
                        
                except Exception as e:
                    print(f"         ❌ Failed to process clip: {e}")
                    continue
            
            if not clips:
                print("   ❌ No valid clips produced")
                return None
            
            # STEP 1.5: CINEMATIC COLOR GRADING
            print(f"      🎨 Applying Color Grade: {production_plan.get('style', 'Standard')}")
            style = production_plan.get('style', '').lower()
            
            processed_clips = []
            for clip in clips:
                # Noir Mode
                if "noir" in style or "black and white" in style:
                    clip = clip.fx(vfx.blackwhite)
                    clip = clip.fx(vfx.colorx, 1.2) # High contrast
                
                # Matrix / Sci-Fi
                elif "cyberpunk" in style or "matrix" in style:
                    # Tint Green/Cyan (R, G, B factor)
                    clip = clip.fx(vfx.colorx, 1.2) # Boost contrast
                    # This is a rough approximation without advanced RGB curves
                    
                # Warm / Nostalgic
                elif "vintage" in style or "warm" in style:
                    # Warmth is hard without curves, but we can assume 'colorx' boosts saturation
                    clip = clip.fx(vfx.colorx, 1.1)
                
                processed_clips.append(clip)
            
            clips = processed_clips
            
            # STEP 2: CONCATENATION
            print("      🎬 Concatenating...")
            final_video = concatenate_videoclips(clips, method="compose")
            
            # STEP 3: AUDIO MIXING (Smart Levels)
            print("      🎧 Mixing Audio Layers...")
            audio_layers = []
            
            # Determine mix levels
            music_vol = 0.25 if voiceover_path else 0.6  # Ducking logic: 25% if VO exists, else 60%
            sfx_vol = 0.6
            vo_vol = 1.0
            
            # Layer 1: Background Music
            if audio_path and os.path.exists(audio_path):
                try:
                    music = AudioFileClip(audio_path)
                    if music.duration < final_video.duration:
                         # Simple loop: just play it again? MoviePy looping is tricky.
                         # Better: fade out if too short
                         pass 
                    else:
                        music = music.subclip(0, final_video.duration)
                    
                    music = music.volumex(music_vol)
                    music = music.audio_fadein(2).audio_fadeout(2) # Smooth transitions
                    audio_layers.append(music)
                    print(f"         ✅ Music Added (Level: {music_vol})")
                except Exception as e:
                    print(f"         ⚠️ Music Failed: {e}")
            
            # Layer 2: Sound Effects
            if sound_effects:
                for sfx_path in sound_effects:
                    if os.path.exists(sfx_path):
                        try:
                            sfx = AudioFileClip(sfx_path).volumex(sfx_vol)
                            if sfx.duration > final_video.duration:
                                sfx = sfx.subclip(0, final_video.duration)
                            audio_layers.append(sfx)
                        except:
                            pass
            
            # Layer 3: Voiceover
            if voiceover_path and os.path.exists(voiceover_path):
                try:
                    vo = AudioFileClip(voiceover_path).volumex(vo_vol)
                    if vo.duration > final_video.duration:
                        vo = vo.subclip(0, final_video.duration)
                    audio_layers.append(vo)
                    print(f"         ✅ Voiceover Added (Level: 1.0)")
                except:
                    pass
            
            if audio_layers:
                final_audio = CompositeAudioClip(audio_layers)
                final_video = final_video.set_audio(final_audio)
            
            # STEP 4: EXPORT
            print(f"      💾 Exporting to {self.output_filename}...")
            final_video.write_videofile(
                self.output_path,
                fps=FPS,
                codec='libx264',
                audio_codec='aac',
                threads=4,
                logger=None
            )
            
            # Cleanup
            final_video.close()
            for c in clips: c.close()
            
            return self.output_path
            
        except Exception as e:
            print(f"   ❌ Editor Critical Error: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _resize_to_1080p(self, clip):
        """Standardize clip to 1920x1080 with proper cropping/resizing"""
        target_w, target_h = 1920, 1080
        
        # Calculate aspect ratios
        clip_ratio = clip.w / clip.h
        target_ratio = target_w / target_h
        
        # Resize logic
        if clip_ratio > target_ratio:
            # Clip is wider - resize by height, crop width
            new_h = target_h
            new_w = int(clip.w * (target_h / clip.h))
            clip = clip.resize(height=new_h)
            # Center crop
            center_x = new_w / 2
            clip = clip.crop(x1=center_x - target_w/2, width=target_w)
        else:
            # Clip is taller - resize by width, crop height
            new_w = target_w
            new_h = int(clip.h * (target_w / clip.w))
            clip = clip.resize(width=new_w)
            # Center crop
            center_y = new_h / 2
            clip = clip.crop(y1=center_y - target_h/2, height=target_h)
            
        return clip

    def _apply_ken_burns(self, clip, duration):
        """Apply cinematic slow zoom/pan effect"""
        # Randomly choose Zoom In or Zoom Out
        zoom_direction = random.choice(['in', 'out'])
        
        def zoom_in(t):
            return 1 + 0.1 * (t / duration)  # 1.0 -> 1.1
            
        def zoom_out(t):
            return 1.1 - 0.1 * (t / duration) # 1.1 -> 1.0
            
        zoom_func = zoom_in if zoom_direction == 'in' else zoom_out
        
        # Apply Resize
        return clip.resize(zoom_func)

    def _create_text_overlay(self, text, duration):
        """Create a text overlay using PIL (No ImageMagick required)"""
        from PIL import Image, ImageDraw, ImageFont
        import numpy as np
        
        w, h = 1920, 1080
        # Create transparent image
        img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Font (fallback to default if not found)
        try:
            # Try to load a bold font
            font = ImageFont.truetype("arialbd.ttf", 80)
        except:
            font = ImageFont.load_default()
            
        # text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        # Position (Bottom Center with margin)
        x = (w - text_w) // 2
        y = h - text_h - 150
        
        # Draw Shadow
        draw.text((x+4, y+4), text, font=font, fill=(0, 0, 0, 180))
        # Draw Text
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        
        # Convert to numpy
        img_np = np.array(img)
        
        # Create ImageClip
        txt_clip = ImageClip(img_np).set_duration(duration)
        return txt_clip

    def _apply_text_overlay(self, clip, text, duration):
        """Composite text over video"""
        if not text or len(text) < 2:
            return clip
        
        try:
            txt_clip = self._create_text_overlay(text, duration)
            return CompositeVideoClip([clip, txt_clip])
        except Exception as e:
            print(f"      ⚠️ Text Overlay Failed: {e}")
            return clip
