import asyncio
import json
import re
import vertexai
import vertexai.preview.generative_models as generative_models
from vertexai.generative_models import GenerativeModel
from app.util.template import TemplateManager
from app.config.config_instance import ConfigInstance
from app.config.config import VARS
from app.logger.logger import LoggerInstance


class VertexFacade:
    """
    Clase para manejar la interacción con el modelo de lenguaje de Google Vertex AI."""
    def __init__(self):
        self.project = ConfigInstance.get(VARS.GCP_VERTEX_PROJECT_ID)
        self.location = ConfigInstance.get(VARS.GCP_VERTEX_LOCATION)
        vertexai.init(project=self.project, location=self.location)
        self.model_name = ConfigInstance.get(VARS.GCP_VERTEX_LLM_MODEL)
        self.template_manager = TemplateManager()
        self.generation_config = {
            "max_output_tokens": int(
                ConfigInstance.get(VARS.GCP_VERTEX_MAX_OUT_TOKENS)
            ),
            "temperature": float(ConfigInstance.get(VARS.GCP_VERTEX_TEMPERATURE)),
            "top_p": float(ConfigInstance.get(VARS.GCP_VERTEX_TOP_P)),
        }
        self.safety_settings = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }

    async def run_prompt(self, text: str) -> str:
        """
        Método para invocar el modelo de lenguaje y obtener una respuesta."""
        try:
            model = GenerativeModel(self.model_name)
            chat = model.start_chat()
            response = await asyncio.to_thread(
                chat.send_message,
                json.dumps(text, ensure_ascii=False),
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
            )
            return response.text if hasattr(response, "text") else str(response)
        except Exception as e:
            LoggerInstance.error(str(e))
            raise
