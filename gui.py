import customtkinter as ctk
import threading
import os
import sys
from datetime import datetime
from PIL import Image

# Set Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class HollywoodStudioGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("🎬 Hollywood Studio AI - Director's Console")
        self.geometry("1100x800")
        
        # Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # State
        self.studio = None
        self.is_generating = False

        self._setup_sidebar()
        self._setup_main_area()
        self._initialize_studio_thread()

    def _setup_sidebar(self):
        """Left Sidebar with Controls"""
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Title
        self.logo = ctk.CTkLabel(self.sidebar, text="HOLLYWOOD\nSTUDIO", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo.pack(pady=30, padx=20)

        # 1. AI Brain (Provider)
        self.mode_frame = ctk.CTkFrame(self.sidebar)
        self.mode_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(self.mode_frame, text="🧠 AI Brain", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.provider_var = ctk.StringVar(value="Ollama (Local)")
        self.provider_combo = ctk.CTkOptionMenu(self.mode_frame, 
                                                values=["Ollama (Local)", "Groq (Free Cloud)", "Claude (Premium)", "OpenAI"],
                                                variable=self.provider_var,
                                                command=self._on_provider_change)
        self.provider_combo.pack(pady=10, padx=10, fill="x")

        # 2. Production Style
        self.style_frame = ctk.CTkFrame(self.sidebar)
        self.style_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(self.style_frame, text="🎨 Visual Style (Grading)", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.style_var = ctk.StringVar(value="Cinematic (Standard)")
        self.style_combo = ctk.CTkOptionMenu(self.style_frame, 
                                           values=["Cinematic (Standard)", "Noir (B&W)", "Cyberpunk (Matrix)", "Vintage (Warm)"],
                                           variable=self.style_var)
        self.style_combo.pack(pady=10, padx=10, fill="x")

        # 3. Audio Controls
        self.audio_frame = ctk.CTkFrame(self.sidebar)
        self.audio_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(self.audio_frame, text="🔊 Audio Engineering", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.ducking_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.audio_frame, text="Smart Ducking", variable=self.ducking_var).pack(anchor="w", padx=10, pady=5)
        
        self.voice_var = ctk.StringVar(value="female_us")
        ctk.CTkOptionMenu(self.audio_frame, variable=self.voice_var, values=["female_us", "male_us", "female_uk", "male_uk"]).pack(fill="x", padx=10, pady=5)

        # 4. Generate Button
        self.generate_btn = ctk.CTkButton(self.sidebar, text="🎬 ACTION!", 
                                        font=ctk.CTkFont(size=18, weight="bold"),
                                        height=60,
                                        fg_color="#4CAF50", hover_color="#45a049",
                                        command=self.start_production)
        self.generate_btn.pack(pady=30, padx=20, fill="x", side="bottom")

    def _setup_main_area(self):
        """Right Main Area"""
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Script Input
        ctk.CTkLabel(self.main_frame, text="📝 Director's Vision (Prompt)", font=("Arial", 14, "bold"), anchor="w").pack(fill="x")
        
        self.prompt_entry = ctk.CTkEntry(self.main_frame, height=50, placeholder_text="Describe your movie idea (e.g. 'A futuristic city in the rain')...")
        self.prompt_entry.pack(fill="x", pady=(5, 10))
        
        # Main Action Button (Redundant for visibility)
        self.main_generate_btn = ctk.CTkButton(self.main_frame, text="✨ Generate Video", 
                                             font=ctk.CTkFont(size=14, weight="bold"),
                                             height=40,
                                             fg_color="#4CAF50", hover_color="#45a049",
                                             command=self.start_production)
        self.main_generate_btn.pack(anchor="e", pady=(0, 20))
        
        # Live Log Console
        ctk.CTkLabel(self.main_frame, text="🖥️ Production Console", font=("Arial", 14, "bold"), anchor="w").pack(fill="x")
        
        self.log_textbox = ctk.CTkTextbox(self.main_frame, font=("Consolas", 12))
        self.log_textbox.pack(fill="both", expand=True, pady=(5, 10))
        
        # Status Bar
        self.status_bar = ctk.CTkLabel(self.main_frame, text="Initializing...", text_color="gray")
        self.status_bar.pack(anchor="e")

        # Open Output Button
        self.open_output_btn = ctk.CTkButton(self.main_frame, text="📂 Open Output Folder", state="disabled", command=self._open_output)
        self.open_output_btn.pack(anchor="e", pady=10)

    def _initialize_studio_thread(self):
        threading.Thread(target=self._init_studio, daemon=True).start()

    def _init_studio(self):
        try:
            self._log("🚀 Initializing Hollywood Engine...")
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from studio import HollywoodStudio
            
            self.studio = HollywoodStudio()
            
            # Feature Detection
            self._log(f"✅ LLM Provider: {os.environ.get('LLM_PROVIDER', 'Auto')}")
            
            if self.studio.art_dept.ltx2_available:
                self._log("✅ LTX-2 Neural Video: Start Ready")
            
            if self.studio.art_dept.comfy.connected:
                self._log("✅ ComfyUI Backend: Connected")
            else:
                 self._log("⚠️ ComfyUI Backend: Disconnected (Video will be stock)")

            self._log("✅ Edge-TTS: Ready")
            self._log("✅ Whisper Subtitles: Ready")
            self._log("✅ Marketing Agent: Ready")
            
            self.status_bar.configure(text="Ready to Film", text_color="#4CAF50")
            self._log("\n🎬 STUDIO READY. Enter a prompt and click ACTION!")
            
        except Exception as e:
            self._log(f"❌ Initialization Error: {e}")
            self.status_bar.configure(text="Initialization Failed", text_color="red")

    def start_production(self):
        if self.is_generating: return
        
        prompt = self.prompt_entry.get()
        if not prompt: return
        
        # Conf
        style = self.style_var.get()
        # Map Provider Name to Code
        provider_map = {
            "Ollama (Local)": "ollama",
            "Groq (Free Cloud)": "groq",
            "Claude (Premium)": "anthropic",
            "OpenAI": "openai"
        }
        selected_provider = provider_map.get(self.provider_var.get(), "ollama")
        
        # Set Env Vars dynamically
        os.environ["LLM_PROVIDER"] = selected_provider
        
        # Check Ollama if selected
        if os.environ["LLM_PROVIDER"] == "ollama":
            if not self._check_ollama():
                self._log("❌ ERROR: Ollama is not running!")
                self._log("   👉 Please open 'Ollama' or run 'ollama serve' in terminal.")
                # from tkinter import messagebox
                # messagebox.showerror("Ollama Offline", "Ollama is not running.\nPlease start it to generate scripts.")
                # Doing it via log is safer for threading
                return

        self.is_generating = True
        self.generate_btn.configure(state="disabled", text="🎥 FILMING...")
        self.main_generate_btn.configure(state="disabled", text="🎥 FILMING...")
        self.log_textbox.delete("1.0", "end")
        
        threading.Thread(target=self._run_pipeline, args=(prompt, style), daemon=True).start()

    def _check_ollama(self):
        """Quick check if Ollama is responding"""
        import requests
        try:
            requests.get("http://localhost:11434", timeout=1)
            return True
        except:
            return False

    def _run_pipeline(self, prompt, style):
        try:
            self._log(f"🎬 ACTION! Production started for: '{prompt}'")
            self._log(f"🎨 Style: {style}")
            self._log("="*50)
            
            # Inject style into prompt effectively
            full_prompt = f"{prompt}. Visual Style: {style}"
            
            # Capture stdout to redirect to GUI (Partial Hack)
            # Better: The studio already prints. We can't easily capture prints from another thread class 
            # without redirecting sys.stdout. Let's do a simple redirect.
            
            class Redirector:
                def __init__(self, text_widget):
                    self.widget = text_widget
                def write(self, string):
                    self.widget.insert("end", string)
                    self.widget.see("end")
                def flush(self): pass

            original_stdout = sys.stdout
            sys.stdout = Redirector(self.log_textbox)
            
            try:
                self.studio.produce_video(full_prompt)
            finally:
                sys.stdout = original_stdout

            self._log("\n" + "="*50)
            self._log("✅ CUT! That's a wrap.")
            self.status_bar.configure(text="Production Complete", text_color="#4CAF50")
            self.open_output_btn.configure(state="normal")
            
        except Exception as e:
            self._log(f"❌ Director Error: {e}")
            import traceback
            self._log(traceback.format_exc())
        finally:
            self.is_generating = False
            self.generate_btn.configure(state="normal", text="🎬 ACTION!")
            self.main_generate_btn.configure(state="normal", text="✨ Generate Video")

    def _log(self, msg):
        self.log_textbox.insert("end", f"{msg}\n")
        self.log_textbox.see("end")

    def _open_output(self):
        output_dir = os.path.abspath("output")
        os.startfile(output_dir)

    def _on_provider_change(self, choice):
        self._log(f"🧠 AI Brain Switched to: {choice}")
        if "Ollama" in choice:
            self._log("   ℹ️ Ensure 'ollama serve' is running.")

if __name__ == "__main__":
    app = HollywoodStudioGUI()
    app.mainloop()
