"""
Enhanced Voiceover Agent - Using Microsoft Edge TTS
Professional text-to-speech with natural voices, no MoviePy timing errors
"""
import os
import asyncio
from config import OUTPUT_DIR

class VoiceoverAgent:
    """
    Creates professional voiceover using Microsoft Edge TTS.
    Generates WAV format for perfect MoviePy compatibility.
    """
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Available voices (Microsoft Edge TTS)
        self.voices = {
            "female_us": "en-US-AriaNeural",
            "male_us": "en-US-GuyNeural",
            "female_uk": "en-GB-SoniaNeural",
            "male_uk": "en-GB-RyanNeural"
        }
        self.default_voice = "female_us"
    
    async def _generate_speech_async(self, text, output_path, voice):
        """Async function to generate speech using Edge TTS"""
        try:
            import edge_tts
            
            communicate = edge_tts.Communicate(text, self.voices[voice])
            await communicate.save(output_path)
            return True
        except ImportError:
            print("   ⚠️ edge-tts not installed. Run: pip install edge-tts")
            return False
        except Exception as e:
            print(f"   ❌ Edge TTS error: {e}")
            return False
    
    def create_voiceover(self, script_scenes, voice="female_us"):
        """
        Generates voiceover from script scenes using Edge TTS.
        
        Args:
            script_scenes: List of scene dictionaries with 'voiceover' text
            voice: Voice preset (female_us, male_us, female_uk, male_uk)
        
        Returns:
            Path to voiceover audio file (WAV format)
        """
        print("   🎙️ Creating voiceover with Microsoft Edge TTS...")
        
        # Combine all voiceover text
        voiceover_text = ""
        for i, scene in enumerate(script_scenes):
            vo = scene.get('voiceover', '')
            if vo:
                voiceover_text += vo + ". "  # Add pause between scenes
        
        if not voiceover_text.strip():
            print("   ⚠️ No voiceover text in script - skipping")
            return None
        
        print(f"   📝 Voiceover text: {len(voiceover_text)} characters")
        print(f"   🎤 Voice: {voice} ({self.voices.get(voice, 'default')})")
        
        try:
            # Output as WAV for better MoviePy compatibility
            output_path = os.path.join(self.output_dir, "voiceover.wav")
            
            # Run async generation
            success = asyncio.run(
                self._generate_speech_async(voiceover_text, output_path, voice)
            )
            
            if success and os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024  # KB
                print(f"   ✅ Voiceover generated: {os.path.basename(output_path)} ({file_size:.1f}KB)")
                return output_path
            else:
                print("   ❌ Voiceover generation failed")
                return None
            
        except Exception as e:
            print(f"   ❌ Voiceover generation failed: {e}")
            return None
    
    def create_short_vo(self, text, voice="female_us"):
        """
        Create short voiceover snippet (for testing or short phrases).
        
        Args:
            text: Text to speak
            voice: Voice preset
        
        Returns:
            Path to voiceover file
        """
        try:
            output_path = os.path.join(self.output_dir, "vo_snippet.wav")
            success = asyncio.run(
                self._generate_speech_async(text, output_path, voice)
            )
            return output_path if success else None
        except Exception as e:
            print(f"   ❌ Short VO failed: {e}")
            return None
    async def _generate_scene_audio(self, scene_text, scene_index, voice):
        """Generates audio for a single scene"""
        filename = f"vo_scene_{scene_index}_{voice}.wav"
        output_path = os.path.join(self.output_dir, filename)
        
        if await self._generate_speech_async(scene_text, output_path, voice):
            return output_path
        return None

    def generate_scene_voiceovers(self, script_scenes, voice="female_us"):
        """
        Generates individual voiceover files for each scene.
        Returns the modified scenes list with 'voiceover_path' added.
        """
        print(f"   🎙️ Generating per-scene voiceovers ({voice})...")
        
        import asyncio
        updated_scenes = []
        
        for i, scene in enumerate(script_scenes):
            text = scene.get('voiceover', '')
            if text:
                print(f"      🗣️ Scene {i+1}: {text[:30]}...")
                # Run async generation for this scene
                path = asyncio.run(self._generate_scene_audio(text, i+1, voice))
                if path:
                    scene['voiceover_path'] = path
                    # Optional: Get duration to update scene length?
                    # For now just save the path.
            updated_scenes.append(scene)
            
        return updated_scenes
