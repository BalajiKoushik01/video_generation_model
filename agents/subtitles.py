import os
import torch
import warnings
from config import OUTPUT_DIR

# Suppress warnings
warnings.filterwarnings("ignore")

class SubtitlesAgent:
    def __init__(self):
        print("   📝 Initializing Local Subtitles Agent (Whisper)...")
        self.available = False
        
        # Check for FFmpeg first
        import shutil
        if not shutil.which("ffmpeg"):
            print("   ⚠️ FFmpeg not found. Subtitles disabled.")
            print("   👉 Install FFmpeg to enable auto-subtitles: https://ffmpeg.org/download.html")
            return

        try:
            import whisper
            # Load small model for speed, medium for quality. 'base' is good compromise for CPU.
            self.model = whisper.load_model("base")
            self.available = True
            print("   ✅ Whisper Model Loaded (Local)")
        except Exception as e:
            print(f"   ⚠️ Whisper error: {e}")
            self.available = False

    def generate_subtitles(self, audio_path):
        """
        Generates .srt subtitles for the given audio file using local Whisper.
        """
        if not self.available or not audio_path or not os.path.exists(audio_path):
            return None

        print(f"   🗣️ Transcribing audio: {os.path.basename(audio_path)}...")
        try:
            # Transcribe
            result = self.model.transcribe(audio_path)
            segments = result["segments"]

            # Save as SRT
            srt_filename = os.path.splitext(os.path.basename(audio_path))[0] + ".srt"
            srt_path = os.path.join(OUTPUT_DIR, srt_filename)

            with open(srt_path, "w", encoding="utf-8") as srt:
                for idx, segment in enumerate(segments):
                    start = self._format_timestamp(segment["start"])
                    end = self._format_timestamp(segment["end"])
                    text = segment["text"].strip()
                    
                    srt.write(f"{idx + 1}\n")
                    srt.write(f"{start} --> {end}\n")
                    srt.write(f"{text}\n\n")
            
            print(f"   ✅ Subtitles saved: {srt_filename}")
            return srt_path

        except Exception as e:
            print(f"   ❌ Transcription Failed: {e}")
            return None

    def _format_timestamp(self, seconds):
        """Converts seconds to SRT timestamp format (HH:MM:SS,mmm)"""
        whole_seconds = int(seconds)
        milliseconds = int((seconds - whole_seconds) * 1000)
        
        hours = whole_seconds // 3600
        minutes = (whole_seconds % 3600) // 60
        seconds = whole_seconds % 60
        
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
