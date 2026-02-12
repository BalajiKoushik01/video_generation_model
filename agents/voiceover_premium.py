import os
import time
import requests
import json
from pathlib import Path
import subprocess
try:
    import edge_tts
    import asyncio
except ImportError:
    edge_tts = None

from config import (
    VOICEOVER_PROVIDER, VOICEOVER_VOICE,
    ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID,
    OPENAI_TTS_MODEL, OPENAI_TTS_VOICE,
    OPENAI_API_KEY
)

class PremiumVoiceoverAgent:
    def __init__(self):
        self.provider = VOICEOVER_PROVIDER
        print(f"🎙️ Premium Voiceover Agent initialized (Provider: {self.provider})")

    def generate_voiceover(self, text, output_path):
        """Generates voiceover using the configured provider."""
        if not text:
            return None

        print(f"   🎙️ Generating voiceover: '{text[:30]}...'")
        
        # Try Primary Provider
        success = False
        if self.provider == "elevenlabs":
            success = self._generate_elevenlabs(text, output_path)
        elif self.provider == "openai":
            success = self._generate_openai(text, output_path)
        elif self.provider == "edge-tts":
            success = self._generate_edge_tts(text, output_path)
        
        # Fallback to Edge-TTS if premium failed (and wasn't already tried)
        if not success and self.provider != "edge-tts":
            print("   ⚠️ Primary provider failed. Falling back to Edge-TTS (Free High-Quality)...")
            success = self._generate_edge_tts(text, output_path)

        if success:
            return output_path
        else:
            print("   ❌ Voiceover generation failed.")
            return None

    def _generate_elevenlabs(self, text, output_path):
        if not ELEVENLABS_API_KEY:
            print("   ⚠️ ElevenLabs API Key missing!")
            return False
            
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"   ❌ ElevenLabs Error: {response.text}")
                return False
        except Exception as e:
            print(f"   ❌ ElevenLabs Exception: {e}")
            return False

    def _generate_openai(self, text, output_path):
        if not OPENAI_API_KEY:
             print("   ⚠️ OpenAI API Key missing!")
             return False
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            
            response = client.audio.speech.create(
                model=OPENAI_TTS_MODEL,
                voice=OPENAI_TTS_VOICE,
                input=text
            )
            
            response.stream_to_file(output_path)
            return True
        except ImportError:
            print("   ⚠️ OpenAI library not installed. Run `pip install openai`")
            return False
        except Exception as e:
             print(f"   ❌ OpenAI TTS Error: {e}")
             return False

    def _generate_edge_tts(self, text, output_path):
        """Uses edge-tts (free) via CLI subprocess (most reliable method)"""
        try:
            # We use subprocess to avoid async complications in synchronous workflow
            cmd = [
                "edge-tts",
                "--voice", VOICEOVER_VOICE,
                "--text", text,
                "--write-media", output_path
            ]
            
            # Run silently
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            return True
            
        except FileNotFoundError:
             print("   ⚠️ edge-tts not found! Please run: pip install edge-tts")
             return False
        except subprocess.CalledProcessError as e:
             print(f"   ❌ Edge-TTS Error: {e}")
             return False
        except Exception as e:
             print(f"   ❌ Edge-TTS Exception: {e}")
             return False

# Test
if __name__ == "__main__":
    agent = PremiumVoiceoverAgent()
    agent.generate_voiceover("This is a test of the Hollywood Studio voiceover system.", "test_voice.mp3")
