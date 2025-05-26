from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from app.models.agent_models import InputBulkModel, InputModel, OutputModel
from app.factory.ai_factory import AIFactory, get_ai_facade_factory
from app.services.bulk_content_service import BulkContentService
from app.services.notion_service import NotionService, get_notion_instance
from app.services.pre_hook_service import get_pre_hook_service, PreHookService
from app.services.agent_chat_services import AgentChatServices
from app.services.contex_chatbot import ContexChatbotService, get_contex_chatbot_service
from app.services.vector_db_service_qdrant import VectorDBServiceInstanceQdrant, VectorDBServiceQdrant

security = HTTPBearer()

RESOURCE = "/agent"
agent_router = APIRouter(prefix=RESOURCE)


async def get_ai_service(
    factory: AIFactory = Depends(get_ai_facade_factory),
    pre_hook_service: PreHookService = Depends(get_pre_hook_service),
    contex_chatbot_service: ContexChatbotService = Depends(get_contex_chatbot_service),
):
    return AgentChatServices(factory, pre_hook_service, contex_chatbot_service)

async def get_bulk_content_service(
    notion_service: NotionService = Depends(get_notion_instance)):
    return BulkContentService(notion_service)

@agent_router.post("/inference", status_code=200)
async def invoke(
    modal_input: InputModel,
    agent_service: AgentChatServices = Depends(get_ai_service)
) -> OutputModel:
    """
    Invoke the agent service with the provided input.
    """
    response = await agent_service.ainvoke(modal_input)
    return OutputModel(answer=response)

@agent_router.post("/bulk-insert", status_code=200)
async def bulk_insert(
    modal_input: InputBulkModel,
    bulk_content_service: BulkContentService = Depends(get_bulk_content_service)
) -> dict:
    """
    Bulk insert content from Notion to Qdrant.
    """
    return await bulk_content_service.bulk_insert(
        collection_name=modal_input.collection_name,
        embedding_algorithm=modal_input.embedding_algorithm)
