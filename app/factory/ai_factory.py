from app.constants.agentModel import VERTEX_AI_MODEL
from app.logger.logger import LoggerInstance
from app.facade.vertex_facade import VertexFacade


class AIFactory:
    """
    Factory para la creación de instancias de IA.

    Métodos:
        create_ia(provider: str): Crea y retorna una instancia de la IA correspondiente al proveedor especificado.
    """

    @staticmethod
    def create_ia(provider: str):
        """
        Crea y retorna una instancia de la IA según el proveedor especificado.

        Parámetros:
            provider (str): Nombre del proveedor de IA.

        Retorna:
            object: Una instancia del proveedor de IA correspondiente.

        Lanza:
            Exception: Si el proveedor no está soportado.
        """
        if provider == VERTEX_AI_MODEL:
            LoggerInstance.info(f"Setting LLM service: {provider}")
            return VertexFacade()


async def get_ai_facade_factory():
    """
    Retorna una instancia de AIFacadeFactory, cacheada para no ser recreada.

    Retorna:
        AIFactory: Una instancia de la fábrica de IA.
    """
    return AIFactory()
