import base64
from app.factory.ai_factory import AIFactory
from app.models.agent_models import InputModel
from app.logger.logger import LoggerInstance
from app.services.pre_hook_service import PreHookService
from app.services.contex_chatbot import ContexChatbotService

class AgentChatServices:
    """
    Clase para manejar la interacción con el modelo de lenguaje y la creación de consultas."""
    def __init__(
        self,
        factory: AIFactory,
        pre_hook_service: PreHookService,
        contex_chatbot_service: ContexChatbotService,
    ):
        self.facade = None
        self.factory = factory
        self.pre_hook_service = pre_hook_service
        self.history = [str]
        self.contex_chatbot_service = contex_chatbot_service

    async def pre_inference(self, modal_input: InputModel):
        """
        Método para obtener los vecinos más cercanos antes de la inferencia.
        """
        LoggerInstance.info("PRE HOOK INVOKED")
        neighbors = await self.pre_hook_service.get_nearest_neighbors(
            query=modal_input.text,
            embedding_algorithm=modal_input.embeddingAlgorithm,
            top_k=modal_input.vectorsTopK,
        )
        return neighbors

    async def ainvoke(self, modal_input: InputModel) -> str:
        """
        Método para invocar el modelo de lenguaje y obtener una respuesta."""
        agent_description_b64 = modal_input.llmAgentDescription
        decoded_bytes = base64.b64decode(agent_description_b64)
        agent_description = decoded_bytes.decode("utf-8")
        neighbors = await self.pre_inference(modal_input)
        prompt_json = await self.contex_chatbot_service.create_query(
            modal_input, agent_description, neighbors)
        print('prompt_json: ', prompt_json)
        self.facade = self.factory.create_ia(modal_input.modelProvider)
        if not self.facade:
            raise ValueError("Invalid model provider specified.")
        system_response_llm = await self.facade.run_prompt(prompt_json)
        return system_response_llm
