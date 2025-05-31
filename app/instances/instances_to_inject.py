from fastapi import Depends

from app.database.qdrant import Qdrant, get_vector_db_service_qdrant
from app.facade.ollama_facade import OllamaClient, get_ollama_client
from app.facade.open_ai_facade import OpenAIFacade, get_open_ai_facade
from app.facade.openrouter_facade import OpenRouterFacade, get_open_router_facade
from app.facade.vertex_facade import VertexFacade, get_vertex_facade
from app.factory.ai_factory import AI_Handdler
from app.services.agent_chat_services import AgentChatServices
from app.services.bulk_content_service import BulkContentService
from app.services.prompt_service import PromptService, get_contex_chatbot_service
from app.services.notion_service import NotionService, get_notion_instance
from app.services.knowledge_service import KnowledgeService
from app.services.vector_db_service import VectorDBService


async def get_vector_db_service(
    vector_database: Qdrant = Depends(get_vector_db_service_qdrant)
)-> VectorDBService:
    """Returns an instance of VectorDBService, cached to avoid recreation."""
    return VectorDBService(vector_database)

async def get_ai_factory(
    # vertex_facade: VertexFacade = Depends(get_vertex_facade),
    open_ai_facade: OpenAIFacade = Depends(get_open_ai_facade),
    open_router_facade: OpenRouterFacade = Depends(get_open_router_facade),
    ollama_client: OllamaClient = Depends(get_ollama_client)
) -> AI_Handdler:
    """Returns an instance of AIFactory, cached to avoid recreation."""
    return AI_Handdler(
        # vertex_facade=vertex_facade,
        open_ai_facade=open_ai_facade,
        open_router_facade=open_router_facade,
        ollama_client=ollama_client
    )

async def get_pre_hook_service(
    vector_db_service: VectorDBService = Depends(get_vector_db_service)
) -> KnowledgeService:
    """Returns an instance of PreHookService, cached to avoid recreation."""
    return KnowledgeService(vector_db_service)

async def get_ai_service(
    factory: AI_Handdler = Depends(get_ai_factory),
    pre_hook_service: KnowledgeService = Depends(get_pre_hook_service),
    contex_chatbot_service: PromptService = Depends(get_contex_chatbot_service),
):
    """Returns an instance of AgentChatServices, cached to avoid recreation."""
    return AgentChatServices(factory, pre_hook_service, contex_chatbot_service)

async def get_bulk_content_service(
    notion_service: NotionService = Depends(get_notion_instance),
    vector_db_service: VectorDBService = Depends(get_vector_db_service)
    ):
    """Returns an instance of BulkContentService, cached to avoid recreation."""
    return BulkContentService(notion_service, vector_db_service)
