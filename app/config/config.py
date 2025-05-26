from enum import Enum
import os
from os import environ as env
from dotenv import load_dotenv

from app.exceptions.exceptions import EnvironmentFileNotFound


class VARS(Enum):
    LOGGING_LEVEL = "LOGGING_LEVEL"
    GCP_VERTEX_LLM_MODEL = "GCP_VERTEX_LLM_MODEL"
    GCP_VERTEX_PROJECT_ID = "GCP_VERTEX_PROJECT_ID"
    GCP_VERTEX_LOCATION = "GCP_VERTEX_LOCATION"
    GCP_VERTEX_MAX_OUT_TOKENS = "GCP_VERTEX_MAX_OUT_TOKENS"
    GCP_VERTEX_TEMPERATURE = "GCP_VERTEX_TEMPERATURE"
    GCP_VERTEX_TOP_P = "GCP_VERTEX_TOP_P"
    
    DEFAULT_CHUNK_SIZE = "DEFAULT_CHUNK_SIZE"
    DEFAULT_CHUNK_OVERLAP_SIZE = "DEFAULT_CHUNK_OVERLAP_SIZE"
    
    NOTION_API_KEY = "NOTION_API_KEY"
    NOTION_PAGE_ID = "NOTION_PAGE_ID"
    
    OPENROUTER_API_KEY = "OPENROUTER_API_KEY"

class Config:
    """
    Config Singleton instance.
    """

    def __init__(self):
        """ENV file ".env" root folder."""
        self._config_data = {}
        self.prompts = {}

        try:
            load_dotenv(override=False)
        except Exception as e:
            raise EnvironmentFileNotFound()
        self.vars = {}
        for VAR in VARS:
            value = env.get(VAR.value)
            if not value:
                from app.logger.logger import LoggerInstance

                LoggerInstance.error(f"Environment variable {VAR.name} wasn't found.")
            self.vars[VAR] = value

    def get(self, varname: VARS) -> str | None:
        return env.get(str(varname)) or self.vars[varname]
