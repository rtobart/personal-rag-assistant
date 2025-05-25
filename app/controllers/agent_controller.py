from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from app.models.agent_models import InputModel, OutputModel
from app.factory.ai_factory import AIFactory, get_ai_facade_factory
from app.services.pre_hook_service import get_pre_hook_service, PreHookService
from app.services.agent_chat_services import AgentChatServices
from app.services.contex_chatbot import ContexChatbotService, get_contex_chatbot_service

security = HTTPBearer()

RESOURCE = "/agent"
agent_router = APIRouter(prefix=RESOURCE)


async def get_ai_service(
    factory: AIFactory = Depends(get_ai_facade_factory),
    pre_hook_service: PreHookService = Depends(get_pre_hook_service),
    contex_chatbot_service: ContexChatbotService = Depends(get_contex_chatbot_service),
):
    return AgentChatServices(factory, pre_hook_service, contex_chatbot_service)


@agent_router.post("/inference", status_code=200)
async def invoke(
    modal_input: InputModel, 
    agent_service: AgentChatServices = Depends(get_ai_service)
) -> OutputModel:
    response = await agent_service.ainvoke(modal_input)
    return OutputModel(answer=response)
