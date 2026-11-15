import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_local_llm(masked_prompt: str, model: str = "qwen2.5-coder:7b") -> str:
    payload = {
        "model": model,
        "prompt": masked_prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "No response from Ollama.")
    except Exception as e:
        return f"Ollama Error: {str(e)}"