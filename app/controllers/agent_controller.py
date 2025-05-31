from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from app.instances.instances_to_inject import get_ai_service, get_bulk_content_service
from app.models.agent_models import InputBulkModel, InputModel, OutputModel
from app.services.bulk_content_service import BulkContentService
from app.services.agent_chat_services import AgentChatServices

security = HTTPBearer()

RESOURCE = "/agent"
agent_router = APIRouter(prefix=RESOURCE)


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
