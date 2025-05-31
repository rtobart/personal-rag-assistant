import base64
from app.factory.ai_factory import AI_Handdler
from app.models.agent_models import InputModel
from app.logger.logger import LoggerInstance
from app.services.knowledge_service import KnowledgeService
from app.services.prompt_service import PromptService

class AgentChatServices:
    """
    Clase para manejar la interacción con el modelo de lenguaje y la creación de consultas."""
    def __init__(
        self,
        factory: AI_Handdler,
        knowledge_service: KnowledgeService,
        prompt_service: PromptService,
    ):
        self.ai_facade = None
        self.factory = factory
        self.knowledge_service = knowledge_service
        self.history = [str]
        self.contex_chatbot_service = prompt_service

    async def ainvoke(self, modal_input: InputModel) -> str:
        """
        Método para invocar el modelo de lenguaje y obtener una respuesta."""
        self.ai_facade = self.factory.instance_ai(modal_input.modelProvider)
        if not self.ai_facade:
            raise ValueError("Invalid model provider specified.")
        agent_description_b64 = modal_input.llmAgentDescription
        decoded_bytes = base64.b64decode(agent_description_b64)
        agent_description = decoded_bytes.decode("utf-8")
        LoggerInstance.info("PRE HOOK INVOKED")
        neighbors = await self.knowledge_service.get_nearest_neighbors(
            query=modal_input.text,
            embedding_algorithm=modal_input.embeddingAlgorithm,
            top_k=modal_input.vectorsTopK,
        )
        prompt_json = await self.contex_chatbot_service.create_query(
            modal_input, agent_description, neighbors)
        system_response_llm = await self.ai_facade.run_prompt(prompt_json)
        return system_response_llm
