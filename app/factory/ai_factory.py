from app.constants.agentModel import VERTEX_AI_MODEL
from app.facade.ollama_facade import OllamaClient
from app.facade.openrouter_facade import OpenRouterFacade
from app.logger.logger import LoggerInstance
from app.facade.vertex_facade import VertexFacade
from app.facade.open_ai_facade import OpenAIFacade


class AI_Handdler:
    def __init__(self,
                # vertex_facade: VertexFacade,
                open_ai_facade: OpenAIFacade,
                open_router_facade: OpenRouterFacade,
                ollama_client: OllamaClient
                ):
        # self.vertex_facade = vertex_facade
        self.open_ai_facade = open_ai_facade
        self.open_router_facade = open_router_facade
        self.ollama_client = ollama_client
    """
    Factory para la creación de instancias de IA.

    Métodos:
        instance_ai(provider: str) -> object:
            Crea y retorna una instancia de la IA según el proveedor especificado.
    """

    def instance_ai(self, provider: str):
        """
        Crea y retorna una instancia de la IA según el proveedor especificado.

        Parámetros:
            provider (str): Nombre del proveedor de IA.

        Retorna:
            object: Una instancia del proveedor de IA correspondiente.

        Lanza:
            Exception: Si el proveedor no está soportado.
        """
        # if provider == VERTEX_AI_MODEL:
        #     LoggerInstance.info(f"Setting LLM service: {provider}")
        #     return self.vertex_facade
        if provider == "openai":
            LoggerInstance.info(f"Setting LLM service: {provider}")
            return self.open_ai_facade
        if provider == "openrouter":
            LoggerInstance.info(f"Setting LLM service: {provider}")
            return self.open_router_facade
        if provider == "ollama":
            LoggerInstance.info(f"Setting LLM service: {provider}")
            return self.ollama_client
        raise Exception(f"Provider {provider} not supported.")


async def get_ai_facade_factory(
    # vertex_facade: VertexFacade = VertexFacade(),
    open_ai_facade: OpenAIFacade = OpenAIFacade(),
    open_router_facade: OpenRouterFacade = OpenRouterFacade(),
    ollama_client: OllamaClient = OllamaClient()
):
    """
    Retorna una instancia de AIFacadeFactory, cacheada para no ser recreada.

    Retorna:
        AIFactory: Una instancia de la fábrica de IA.
    """
    return AI_Handdler(
        # vertex_facade=vertex_facade,
        open_ai_facade=open_ai_facade,
        open_router_facade=open_router_facade,
        ollama_client=ollama_client
    )
