import os
import json
import time
from config import OUTPUT_DIR, RESOLUTION
# Import Agents (Placeholders for now, to be implemented next)
from agents.super_director import SuperDirector
from agents.specialist_directors import (LightingDirector, CinematographyDirector, 
                                          EditingDirector, TransitionsDirector, AudioDirector)
from agents.intelligence import IntelligenceAgent
from agents.workflow_tracker import WorkflowTracker
from agents.screenwriter import ScreenwriterAgent
from agents.art_dept import ArtDeptAgent
from agents.smart_librarian import SmartLibrarianAgent
from agents.editor import EditorAgent
from agents.production import ProductionAgent
from agents.sound_dept import SoundDeptAgent
from agents.sound_effects import SoundEffectsAgent
from agents.color_grading import ColorGradingAgent
from agents.cinematographer import CinematographerAgent # NEW
from agents.voiceover import VoiceoverAgent # NEW

class HollywoodStudio:
    def __init__(self):
        print("🎬 Initializing Hollywood-AI Studio (Hierarchical Director Mode)...")
        print("   🎯 Super Director + 5 Specialist Directors")
        
        # Initialize Super Director (Chief Creative Officer)
        self.super_director = SuperDirector()
        
        # Initialize Specialist Directors
        self.lighting_director = LightingDirector()
        self.cinematography_director = CinematographyDirector()
        self.editing_director = EditingDirector()
        self.transitions_director = TransitionsDirector()
        self.audio_director = AudioDirector()
        
        # Initialize Intelligence layer
        self.intelligence = IntelligenceAgent()
        # Initialize Workflow Tracker (for full awareness)
        self.tracker = WorkflowTracker()
        self.screenwriter = ScreenwriterAgent()
        self.librarian = SmartLibrarianAgent(intelligence=self.intelligence)
        self.art_dept = ArtDeptAgent()
        self.editor = EditorAgent()
        self.production = ProductionAgent()
        self.sound_dept = SoundDeptAgent()
        self.sound_effects = SoundEffectsAgent()
        self.color_grading = ColorGradingAgent()
        self.cinematographer = CinematographerAgent() # NEW
        self.voiceover = VoiceoverAgent() # NEW
        
    def produce_video(self, user_prompt):
        print(f"\n📢 RECEIVED BRIEF: '{user_prompt}'")
        
        # STEP 0: SUPER DIRECTOR - Create Production Plan
        print("\n🎬 SUPER DIRECTOR: Planning production...")
        production_plan = self.super_director.plan_production(user_prompt)
        
        if not production_plan:
            print("⚠️ Super Director failed, falling back to standard workflow...")
            production_plan = None
        
        # Use production plan as script if available
        script = production_plan if production_plan else None
        
        # Step 0.2: Color Grading (Set Visual Mood)
        print("🎨 Color Director: Setting visual mood...")
        color_palette = self.color_grading.generate_palette(mood="cinematic")
        if color_palette:
            print(f"   ✅ Color Scheme: {color_palette['hex'][0]} (Primary)")
            print(f"   💡 Suggested LUT: {self.color_grading.suggest_lut(color_palette)}")
        
        # Step 1: Pre-Production (Scripting)
        print("📝 Step 1: Director is writing the script...")
        script = None
        
        # Check if user provided a custom JSON script
        try:
            custom_script = json.loads(user_prompt)
            if 'shot_list' in custom_script or 'scenes' in custom_script:
                print("   ✅ Custom script detected! Using your detailed script...")
                script = custom_script
                # Normalize key
                if 'shot_list' in script and 'scenes' not in script:
                    script['scenes'] = script['shot_list']
        except (json.JSONDecodeError, TypeError):
            # Not JSON, proceed with AI generation
            pass
        
        # If no custom script, generate one
        if not script:
            try:
                script = json.loads(self.screenwriter.write_script(user_prompt))
                
                # Normalize: Handle both 'scenes' and 'shot_list' keys
                if 'shot_list' in script and 'scenes' not in script:
                    script['scenes'] = script['shot_list']
                
                print(f"   Script Generated: {len(script.get('scenes', []))} scenes.")
                
            except Exception as e:
                print(f"   ⚠️ Screenwriter Error (Check API Key): {e}")
                print("   ⚠️ Configuring Manual Fallback Script (Using Stock Footage)...")
                # Fallback to STOCK so we guarantee an output even if ComfyUI is down
                script = {"scenes": [{"visual_prompt": user_prompt, "duration": 5, "source_type": "STOCK"}]}
        
        # Save Script
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        with open(os.path.join(OUTPUT_DIR, "script.json"), "w") as f:
            json.dump(script, f, indent=4)
        print(f"   💾 Script saved to {OUTPUT_DIR}\\script.json")
        print(f"   📊 Total Scenes: {len(script.get('scenes', []))}")
        
        # Step 1.2: Quality Assessment
        print("🎯 Intelligence: Assessing script quality...")
        quality = self.intelligence.assess_script_quality(script)
        # ... (logging quality)

        # NEW STEP: Cinematographer (Visual Enhancement)
        print("\n🎥 [COMMUNICATION] Screenwriter -> Cinematographer: 'Here is the draft script. Please refine the visuals.'")
        print("   🎥 Cinematographer: 'On it. Adding lens choices and lighting specs...'")
        script = self.cinematographer.enhance_visuals(script)
        print("   🎥 Cinematographer -> Team: 'Visuals locked. Ready for production.'")

        # NEW STEP: Voiceover (Audio Generation)
        print("\n🎙️ [COMMUNICATION] Screenwriter -> Voice Actor: 'Please record the narration for these scenes.'")
        scenes = script.get('scenes', [])
        scenes = self.voiceover.generate_scene_voiceovers(scenes)
        script['scenes'] = scenes # Update script with audio paths
        print("   🎙️ Voice Actor -> Editor: 'Audio files are ready and synced.'")
        
        # Step 2: Casting & Art (Static Visuals & Stock)
        print("\n🎨 [COMMUNICATION] Cinematographer -> Art Dept / Librarian: 'Sourcing visuals based on new specs...'")
        assets = []
        if script and 'scenes' in script:
            for index, scene in enumerate(script['scenes']):
                source = str(scene.get("source_type", "GENERATE")).upper()
                asset_path = None
                was_generated = False

                try:
                    if source == "STOCK":
                        asset_path = self.librarian.get_best_match(scene)
                    else:
                        asset_path = self.art_dept.generate_keyframe(scene)
                        was_generated = bool(asset_path)

                    if not asset_path:
                        # Try the other source. Never append a missing asset.
                        if source == "STOCK":
                            asset_path = self.art_dept.generate_keyframe(scene)
                            was_generated = bool(asset_path)
                        else:
                            asset_path = self.librarian.get_best_match(scene)
                            was_generated = False

                    if not asset_path:
                        print(f"      No usable asset for scene {index + 1}; skipping")
                        continue

                    if was_generated:
                        video_path = self.production.shoot_scene(scene, asset_path)
                        if video_path:
                            asset_path = video_path

                    assets.append({
                        "path": asset_path,
                        "duration": scene.get("duration", 5),
                        "text_overlay": scene.get("text_overlay", ""),
                        "voiceover_path": scene.get("voiceover_path"),
                        "type": "GENERATED" if was_generated else "STOCK",
                    })
                    print(f"      Acquired: {os.path.basename(asset_path)}")
                except Exception as exc:
                    print(f"      Scene {index + 1} asset processing failed: {exc}")

        if not assets:
            raise RuntimeError(
                "No usable scene assets were created; check stock provider "
                "credentials, model availability and input prompts."
            )

        # Step 3.5: Sound Department - CRITICAL AUDIO FIX
        print("🎵 Step 3.5: Composing Original Score...")
        total_duration = len(assets) * 4
        audio_track = self.sound_dept.compose_score(user_prompt, duration=total_duration)
        
        # VALIDATE AUDIO
        if audio_track:
            if not os.path.isabs(audio_track):
                audio_track = os.path.join(OUTPUT_DIR, audio_track)
            
            if os.path.exists(audio_track):
                size_kb = os.path.getsize(audio_track) / 1024
                print(f"      ✅ AUDIO VALIDATED:")
                print(f"         File: {os.path.basename(audio_track)}")
                print(f"         Size: {size_kb:.1f} KB")
                print(f"         Path: {audio_track}")
            else:
                print(f"      ⚠️ Audio path invalid: {audio_track}")
                audio_track = None
        else:
            print(f"      ⚠️ No audio generated")
        
        # Step 3.6: Sound Effects
        print("🔊 Step 3.6: Adding SFX...")
        sound_effects = []
        # Add ambient sound based on first scene
        if script and script.get('scenes'):
            first_scene = script['scenes'][0]
            scene_desc = first_scene.get('visual_prompt', '').lower()
            
            # Detect scene type for ambient sound
            if 'coffee' in scene_desc or 'cafe' in scene_desc:
                sfx = self.sound_effects.get_ambient_sound('coffee shop')
                if sfx: sound_effects.append(sfx)
            elif 'city' in scene_desc or 'street' in scene_desc:
                sfx = self.sound_effects.get_ambient_sound('city')
                if sfx: sound_effects.append(sfx)
            elif 'nature' in scene_desc or 'forest' in scene_desc:
                sfx = self.sound_effects.get_ambient_sound('nature')
                if sfx: sound_effects.append(sfx)

        # Step 4: Post-Production (Upscale & Edit)
        print("🎞️ Step 4: Post-Production is mastering (Final Cut)...")
        
        # Assemble the final video
        print("   🎬 Calling Editor Agent...")
        
        # Ensure audio track path is correct
        if audio_track and not os.path.isabs(audio_track):
            audio_track = os.path.join(OUTPUT_DIR, audio_track)
        
        # Debug audio
        print(f"   🎵 Audio Track: {audio_track if audio_track else 'None'}")
        print(f"   🔊 Sound Effects: {len(sound_effects) if sound_effects else 0} effects")
        
        # Call editor with all audio
        final_video = self.editor.assemble_cut(
            assets,
            audio_path=audio_track,  # Background music
            sound_effects=sound_effects,  # SFX list
            voiceover_path=voiceover_path,  # Voiceover (disabled)
            production_plan={"prompt": user_prompt},
            tracker=self.tracker
        )
        
        # Step 5: Localization & Documentation (No API Extras)
        if final_video:
            # Subtitles (Local Whisper)
            from agents.subtitles import SubtitlesAgent
            subs_agent = SubtitlesAgent()
            if subs_agent.available:
                print("   📝 Generating Subtitles (Auto-Captioning)...")
                # Extract audio from final video for transcribing? 
                # Or transcribe the voiceover file if exists. 
                # Better: Transcribe final video audio to catch everything.
                # Assuming Editor outputs usually have audio. 
                # For simplicity, let's transcribe voiceover track if available, or final video.
                target_audio = voiceover_path if voiceover_path else final_video
                subs_path = subs_agent.generate_subtitles(target_audio)
                if subs_path:
                    print(f"      ✅ Subtitles: {os.path.basename(subs_path)}")

            # Storyboard
            from agents.storyboard import StoryboardAgent
            story_agent = StoryboardAgent()
            # Map scene index to first frame/image
            visual_map = {}
            for asset in assets:
                idx = asset.get('scene_index')
                path = asset.get('path')
                if idx is not None and path:
                    visual_map[idx] = path
            
            story_agent.create_storyboard(script, visual_map)

            # Marketing: Press Kit (Poster + Copy)
            from agents.marketing import MarketingAgent
            marketing = MarketingAgent()
            try:
                marketing.create_press_kit(script)
            except Exception as e:
                print(f"   ⚠️ Marketing Agent failed: {e}")

            print(f"✅ PRODUCTION COMPLETE. Output saved to {final_video}")
            print(f"\n{'='*60}")
            print(f"Full path: {final_video}")
            print(f"{'='*60}")
            # Auto-open the file
            try:
                os.startfile(final_video)
            except:
                pass
        else:
            print(f"⚠️ Production finished but no video could be assembled (check logs).")
            print(f"   Assets are located in {OUTPUT_DIR}")

if __name__ == "__main__":
    studio = HollywoodStudio()
    # studio.produce_video("A cinematic commercial for Bru Coffee. Gold granules, rich aroma, woman enjoying a sip.")
