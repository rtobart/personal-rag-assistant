from openai import OpenAI
import test

from app.config.config import VARS
from app.config.config_instance import ConfigInstance

class OpenAIFacade:
    def __init__(self):
        self.openai_client = OpenAI()

    async def run_prompt(self, text: dict) -> str:
        """
        Método para invocar el modelo de lenguaje y obtener una respuesta.
        """
        print('text: ', text)
        text = str(text)
        try:
            completion = self.openai_client.responses.create(
                    model="gpt-4.1",
                    input="hola",
                )
            response = completion.choices[0].message.content
            return response if response else "No response from OpenAI API"
        except Exception as e:
            raise RuntimeError(f"Error in OpenAI API: {str(e)}")

def get_open_ai_facade():
    """
    Factory function to create an instance of OpenAIFacade.
    """
    return OpenAIFacade()