from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition
from app.config.config_instance import ConfigInstance
from app.exceptions.exceptions import DatabaseConnectionError, DatabaseOffline, InvalidQuery
from app.interfaces.vector_database_interface import VectorDatabaseInterface
from app.logger.logger import LoggerInstance
from app.models.file import FileBatch
from app.models.search import Search

class Qdrant(VectorDatabaseInterface):
    client = None
    def __init__(self):
        self.config = ConfigInstance
        self.connected = False
        self.logger = LoggerInstance
        self.attempts = 0
        self.start()
        self.embedding_default_field_name = "embedding"

    def start(self):
        max_attempts = int(self.config.get("QDRANT_ATTEMPTS"))
        while self.attempts <= max_attempts:
            self.logger.info(
                f"[QDRANT] ATTEMPT {self.attempts} to connect to Qdrant at "
                f"{self.config.get('QDRANT_HOST')}:{self.config.get('QDRANT_PORT')}, DB:{self.config.get('QDRANT_DB_NAME')}"
            )
            try:
                host=str(self.config.get('QDRANT_HOST'))
                port=self.config.get('QDRANT_PORT')
                api_key=self.config.get('QDRANT_API_KEY') or ''
                self.client = QdrantClient(host=host, port=port, api_key=api_key)
                self.connected = True
                self.logger.info(f"CONNECTION ESTABLISHED: {self.test_connection()}")
                self.logger.info(f"[DB] LISTADO COLECCIONES: {self.client.get_collections()}")
                break
            except Exception as e:
                if self.attempts == max_attempts:
                    raise DatabaseConnectionError()
                self.connected = False
                self.logger.error(str(e))
                self.logger.warning("[QDRANT] CONNECTION WASN'T ESTABLISHED CORRECTLY.")
                self.attempts += 1

    def online(self):
        """
          Verify that database connection is online.
          Otherwise, DatabaseOffline exception is raised.
        """
        if not self.client:
            self.connected = False
            self.logger.info("[Qdrant] OFFLINE")
            try:
                self.start()
            except Exception as e:
                self.logger.error(str(e))
                raise DatabaseOffline()
        return self.connected

    def test_connection(self):
        return self.online()

    async def insert_data(self, collection_name: str, files: FileBatch):
        try:
            if not self.client.collection_exists(collection_name):
                self.logger.info(f"La colección '{collection_name}' no existe. Creando colección...")
                vector_size = len(files.file_chunks[0].embedding) if files.file_chunks and files.file_chunks[0].embedding else 1536
                self.client.recreate_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE
                    )
                )
                self.logger.info(f"Colección '{collection_name}' creada exitosamente.")
            point_structs = []
            for index, file_chunk in enumerate(files.file_chunks):
                file_chunk.metadata['content'] = file_chunk.content
                embedding = file_chunk.embedding
                metadata = file_chunk.metadata
                points=PointStruct(id=index, vector=embedding, payload=metadata)
                point_structs.append(points)

            self.client.upsert(
                collection_name=collection_name,
                points=point_structs
            )
            self.logger.info(f"Proceso de inserción de datos en {collection_name} completado.")

        except Exception as e:
            print("error insert_data:", str(e))
            self.logger.error(str(e))
            raise InvalidQuery()

    async def search_text(self, search: Search) -> list[str]:
        if search.filter_property is None or search.filter_property == "":
            return await self.search_text_no_filter(search)
        else:
            return await self.search_text_filter(search)

    async def search_text_filter(self, search: Search) -> list[str]:
        try:
            hits = self.client.search(
            collection_name=search.collection_name,
            query_vector=search.search_embedding,
            query_filter=Filter(
                must=[ 
                        FieldCondition(
                        key=search.filter_property,  # Condition based on values of `column` field.
                        match={"value":search.filter_value}
                        )
                ]
            ),
            limit=search.top_k,  # Return number of closest points
            with_vectors=True,
            )
            return hits
    
        except Exception as e:
            self.logger.error(str(e))
            raise InvalidQuery()

    async def search_text_no_filter(self, search: Search) -> list[str]:
        try:
            hits = self.client.search(
            collection_name=search.collection_name,
            query_vector=search.search_embedding,
            limit=search.top_k,
            with_vectors=True,
            )
            return hits
        except Exception as e:
            self.logger.error(str(e))
            return []

def get_vector_db_service_qdrant() -> Qdrant:
    """Returns an instance of Qdrant, cached to avoid recreation."""
    return Qdrant()
