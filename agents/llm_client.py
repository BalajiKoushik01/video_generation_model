import os
import json
import requests
import time
from config import (
    GROQ_API_KEY, 
    ANTHROPIC_API_KEY, 
    OPENAI_API_KEY, 
    OLLAMA_BASE_URL, 
    OLLAMA_MODEL,
    LLM_PROVIDER
)

class LLMClient:
    """
    Centralized Client for all LLM interactions in Hollywood Studio.
    Supports: Ollama (Local), Groq, Anthropic, OpenAI.
    """
    def __init__(self, provider=None):
        # Allow overriding provider, otherwise use config default
        self.provider = provider or os.getenv("LLM_PROVIDER", LLM_PROVIDER).lower()
        self.max_retries = 3
        
        # Models Configuration
        self.models = {
            "ollama": {
                "default": OLLAMA_MODEL
            },
            "groq": {
                "default": "llama-3.3-70b-versatile",
                "fast": "llama-3.1-8b-instant"
            },
            "anthropic": {
                "default": "claude-3-5-sonnet-20240620"
            },
            "openai": {
                "default": "gpt-4o"
            }
        }
    
    def generate(self, system_prompt, user_prompt, temperature=0.7, json_mode=False, model=None):
        """
        Generic generation method that handles provider differences.
        Returns: String (content) or Dict (if json_mode and parsed successfully)
        """
        # Auto-fallback to Ollama if keys are missing for cloud providers
        if self.provider == "anthropic" and not ANTHROPIC_API_KEY:
            print("⚠️ Claude API Key missing. Falling back to Ollama.")
            self.provider = "ollama"
        elif self.provider == "groq" and not GROQ_API_KEY:
            print("⚠️ Groq API Key missing. Falling back to Ollama.")
            self.provider = "ollama"
        elif self.provider == "openai" and not OPENAI_API_KEY:
             print("⚠️ OpenAI API Key missing. Falling back to Ollama.")
             self.provider = "ollama"

        print(f"🤖 AI Request [{self.provider.upper()}]...")

        try:
            if self.provider == "ollama":
                return self._call_ollama(system_prompt, user_prompt, temperature, json_mode, model)
            elif self.provider == "groq":
                return self._call_open_ai_compat(
                    "https://api.groq.com/openai/v1/chat/completions",
                    GROQ_API_KEY,
                    system_prompt, user_prompt, temperature, json_mode, 
                    model or self.models['groq']['default']
                )
            elif self.provider == "openai":
                return self._call_open_ai_compat(
                    "https://api.openai.com/v1/chat/completions",
                    OPENAI_API_KEY,
                    system_prompt, user_prompt, temperature, json_mode,
                    model or self.models['openai']['default']
                )
            elif self.provider == "anthropic":
                return self._call_anthropic(system_prompt, user_prompt, temperature, json_mode, model)
            else:
                # Default fallback
                return self._call_ollama(system_prompt, user_prompt, temperature, json_mode, model)
                
        except Exception as e:
            print(f"❌ LLM Error ({self.provider}): {e}")
            if self.provider != "ollama":
                print("🔄 Attempting Fallback to Ollama...")
                try:
                    return self._call_ollama(system_prompt, user_prompt, temperature, json_mode, model)
                except Exception as e2:
                    print(f"❌ Fallback Failed: {e2}")
            return None

    def _call_ollama(self, system_prompt, user_prompt, temperature, json_mode, model):
        """Call Local Ollama Instance"""
        url = OLLAMA_BASE_URL
        prompt_content = f"System: {system_prompt}\nUser: {user_prompt}"
        
        # Ollama JSON mode enforcement
        format_param = "json" if json_mode else None
        if json_mode and "JSON" not in prompt_content:
             prompt_content += "\nRESPONSE MUST BE VALID JSON."

        payload = {
            "model": model or self.models['ollama']['default'],
            "prompt": prompt_content,
            "stream": False,
            "format": format_param,
            "options": {
                "temperature": temperature
            }
        }
        print(f"   📤 Sending to Ollama (Model: {payload['model']})...")
        
        try:
            response = requests.post(url, json=payload, timeout=300) # Increased timeout for slow local generation
            if response.status_code == 200:
                res_json = response.json()
                content = res_json.get('response', '')
                if json_mode:
                    return self._clean_and_parse_json(content)
                return content
            else:
                print(f"   ❌ Ollama Error Status: {response.status_code}")
                print(f"   ❌ Ollama Response: {response.text}")
                raise Exception(f"Ollama status {response.status_code}")
        except Exception as e:
            print(f"   ❌ Ollama Exception: {e}")
            raise e

    def _call_open_ai_compat(self, url, key, system_prompt, user_prompt, temperature, json_mode, model):
        """Generic OpenAI-Compatible API Call (Groq, OpenAI)"""
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": 4000
        }
        
        if json_mode:
             payload["response_format"] = {"type": "json_object"}
        
        response = requests.post(url, headers=headers, json=payload, verify=False, timeout=60)
        
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            if json_mode:
                return self._clean_and_parse_json(content)
            return content
        else:
            raise Exception(f"API status {response.status_code}: {response.text}")

    def _call_anthropic(self, system_prompt, user_prompt, temperature, json_mode, model):
        """Call Anthropic API (Claude)"""
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        # Anthropic doesn't support 'response_format: json' natively in the same way, 
        # but we can prompt it.
        if json_mode:
            system_prompt += " Output strictly valid JSON."

        payload = {
            "model": model or self.models['anthropic']['default'],
            "max_tokens": 4096,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            res_json = response.json()
            content = res_json['content'][0]['text']
            if json_mode:
                return self._clean_and_parse_json(content)
            return content
        else:
            raise Exception(f"Anthropic status {response.status_code}: {response.text}")

    def _clean_and_parse_json(self, text):
        """Helper to clean markdown JSON blocks"""
        print(f"   🐛 RAW LLM OUTPUT: {text[:200]}...") # Debug print
        try:
            return json.loads(text)
        except:
            # Clean markdown
            cleaned = text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError as e:
                print(f"   ❌ JSON PARSE ERROR: {e}")
                print(f"   ❌ OFFENDING CONTENT: {cleaned}")
                raise e

