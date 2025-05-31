import httpx
from typing import Optional


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url
        self.model = model
        self.endpoint = f"{self.base_url}/api/generate"
        self.client = httpx.AsyncClient(timeout=500.0)

    async def run_prompt(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        payload = {
            "model": self.model,
            "prompt": f"{prompt}",
            "stream": False
        }
        print('payload: ', payload)

        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = await self.client.post(self.endpoint, json=payload)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except httpx.HTTPError as e:
            print(f"Error communicating with Ollama: {e}")
            return "Error: could not generate response."

    async def close(self):
        await self.client.aclose()
        
def get_ollama_client(base_url: str = "http://localhost:11434", model: str = "llama2") -> OllamaClient:
    """
    Factory function to create an instance of OllamaClient.
    
    Args:
        base_url (str): The base URL for the Ollama API.
        model (str): The model to use for generation.
    
    Returns:
        OllamaClient: An instance of the OllamaClient class.
    """
    return OllamaClient(base_url=base_url, model=model)

