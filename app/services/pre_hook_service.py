import requests
import json
import aiohttp
from datetime import datetime
from app.config.config_instance import ConfigInstance
from app.config.config import VARS
from app.exceptions.exceptions import NearestNeighborException, ProxyEmbeddingException
from app.models.search import Search
from app.services.vector_db_service_qdrant import VectorDBServiceInstanceQdrant
from app.logger.logger import LoggerInstance
from app.services.query_processing import process_query


class PreHookService:

    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    async def get_retrieved_embedding(self, query, embedding_algorithm):
        try:
            body = {"query": [query], "embedding": embedding_algorithm}
            LoggerInstance.info(f"Inicio embeddings {datetime.now()} ")
            res = await process_query(body)
            return res[0]["embedding"]
        except Exception as e:
            LoggerInstance.error(str(e))
            raise ProxyEmbeddingException()

    async def get_retrived_vectors(self, metadata):
        """Realiza la búsqueda de los vectores en la base de datos vectorial."""
        try:
            LoggerInstance.info(f"Inicio vector {datetime.now()} ")
            search_object = Search(
                top_k=metadata["top_k"],
                collection_name=metadata["collection_name"],
                search_text=metadata["search_text"],
                search_embedding=metadata["search_embedding"],
                filter_property=metadata["filter_property"],
                filter_value=metadata["filter_value"],
            )
            LoggerInstance.debug(f"Metadata: {metadata}")
            vectors = VectorDBServiceInstanceQdrant.search_text(search_object)
        except Exception as e:
            LoggerInstance.error(f"Error inesperado: {str(e)}")
            raise NearestNeighborException()

        if not vectors:
            LoggerInstance.info("No se encontraron vectores.")
            return None
        LoggerInstance.info(f"Fin vector {datetime.now()} ")
        context = [
            vector.payload["content"] for vector in vectors if "content" in vector.payload
        ]
        if not context:
            LoggerInstance.info("No se encontraron textos en los vectores.")
            return None
        LoggerInstance.info("Vectores recuperados correctamente.")
        return context

    async def get_nearest_neighbors(self, query, embedding_algorithm, top_k):
        """
        Realiza la búsqueda de los embedding en la base de datos vectorial.

        Args:
            query (str): La consulta que se desea buscar.
        Raises:
            NearestNeighborException: Si ocurre un error durante la ejecución del proceso de recuperación de vectores.
        """
        LoggerInstance.info("-  EXECUTING VECTOR RETRIEVAL...")
        retrieved_embedding = await self.get_retrieved_embedding(
            query, embedding_algorithm
        )

        if retrieved_embedding is None:
            return "No context"

        LoggerInstance.info("- RETRIEVED.")

        metadata = {
            "top_k": top_k,
            "search_text": query,
            "search_embedding": retrieved_embedding,
            "filter_property": "",
            "filter_value": "",
            "collection_name": "notion"
        }
        context = await self.get_retrived_vectors(metadata)
        return context


def get_pre_hook_service() -> PreHookService:
    return PreHookService()
