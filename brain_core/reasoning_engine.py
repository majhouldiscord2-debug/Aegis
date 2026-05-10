import requests
import json

class ReasoningEngine:
    """Orchestrates the reasoning process using Ollama API."""
    
    def __init__(self, model="tinyllama"):
        self.model = model
        self.api_url = "http://localhost:11434/api/chat" # Switched to Chat API

    def reason(self, system_context, user_input):
        """Send messages to the LLM via Chat API."""
        print(f"DEBUG: Model: {self.model}")
        
        messages = [
            {"role": "system", "content": system_context},
            {"role": "user", "content": user_input}
        ]
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "options": {
                "stop": ["USER INPUT:", "RECENT INFO:", "OBSERVATIONS:"],
                "num_thread": 4, # Optimize for multi-core CPUs
                "temperature": 0.2, # Lower temperature = faster, more deterministic
                "num_predict": 128 # Limit response length for speed
            }
        }
        
        full_response = ""
        try:
            print("Thinking", end="", flush=True)
            response = requests.post(self.api_url, json=payload, timeout=300, stream=True)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if "message" in chunk:
                        text = chunk["message"].get("content", "")
                        full_response += text
                        print(".", end="", flush=True)
                    if chunk.get("done"):
                        break
            
            print("\n")
            return full_response.strip()
        except requests.exceptions.Timeout:
            return "\nReasoning Error: Timeout after 300s. The system is extremely slow."
        except requests.exceptions.RequestException as e:
            return f"\nReasoning Error (API): {str(e)}"
        except Exception as e:
            return f"\nReasoning Error (General): {str(e)}"
