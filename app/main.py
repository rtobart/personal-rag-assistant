from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import agent_controller
from app.middlewares.request_wrapper import log_request
from app.logger.logger import LoggerInstance

from contextlib import asynccontextmanager
import httpx


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle context manager to handle startup and shutdown events.
    """
    global client
    # ON STARTUP -----------
    LoggerInstance.info("APPLICATION INIT")
    client = httpx.AsyncClient(
        limits=httpx.Limits(max_connections=30, max_keepalive_connections=20)
    )
    # app insights initialization or other startup tasks
    yield
    # AFTER CLOSE APP
    # await any pending tasks if necessary
    await client.aclose()  # Cierra el cliente cuando la app se apaga
    LoggerInstance.info("APPLICATION SHUTDOWN.")


app = FastAPI(
    title="personal rag assistant",
    description="service to do the inference of the models",
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    LoggerInstance.error(f"Validation error: {exc.errors()} - Body: {exc.body}")
    return JSONResponse(
        status_code=422,
        content={
            "message": "Error de validación",
            "errors": exc.errors(),  # Detalles de los errores
            "body": exc.body,  # Cuerpo original enviado en la solicitud
        },
    )


routes_prefix = "/personal-assistant/api/v1"

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_request_middleware(request, call_next):
    """
    Middleware to log requests.
    """
    return await log_request(request, call_next)


app.include_router(
    agent_controller.agent_router, prefix=routes_prefix, tags=["agent router"]
)

LoggerInstance.info("Creating health check in /health")


@app.head(f"{routes_prefix}/health")
async def health_check():
    """
    Health check endpoint.
    """
    return JSONResponse(status_code=200, content={})
