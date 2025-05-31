from typing import List
from app.logger.logger import LoggerInstance
from app.models.agent_models import InputModel
from app.util.template import TemplateManager

class PromptService:
    """
    Clase para manejar la creación de consultas y la gestión de plantillas."""
    def __init__(self):
        self.template_manager = TemplateManager()

    async def create_query(
        self, input: InputModel, agent_description: str, neighbors: List[str]
    ) -> dict:
        """
        Crea una consulta para el modelo de lenguaje basado 
        en la entrada del usuario y el contexto recuperado."""
        try:
            prompt_json = self.template_manager.get_config()
            prompt_json["contexto_recuperado"].extend(neighbors)
            prompt_json["consulta_del_usuario"] = input.text
            prompt_json["instrucciones"] = agent_description
            return prompt_json
        except Exception as e:
            LoggerInstance.error(f"Error creating query: {e}")
            return {"user_query": input.text}

def get_contex_chatbot_service() -> PromptService:
    """Retorna una instancia de ContexChatbotService, cacheada para no ser recreada."""
    return PromptService()
