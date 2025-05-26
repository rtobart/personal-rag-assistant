from typing import Optional
from openai import OpenAI

from app.config.config import VARS
from app.config.config_instance import ConfigInstance

class OpenRouterFacade:
    def __init__(self):
        self.openai_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=ConfigInstance.get(VARS.OPENROUTER_API_KEY))

    async def run_prompt(self, text: str, setting: Optional[str] = "user") -> str:
        """
        Método para invocar el modelo de lenguaje y obtener una respuesta.
        """
        try:
            completion = self.openai_client.chat.completions.create(
                    model="openai/gpt-4o-mini",
                    messages=[
                        {
                        "role": "user",
                        "content": f"{text}"
                        }
                    ]
                )
            response = completion.choices[0].message.content
            return response if response else "No response from OpenAI API"
        except Exception as e:
            raise RuntimeError(f"Error in OpenRouter API: {str(e)}")