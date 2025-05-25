from app.database.qdrant import QdrantInstance
from app.interfaces.vector_database_interface import VectorDatabaseInterface
from app.models.collection import CollectionDto
from app.models.file import FileBatch
from app.models.search import Search

class VectorDBServiceQdrant:

    def __init__(self, vector_database: VectorDatabaseInterface):
        self.vector_database = vector_database

    def see_connection(self):
        return self.vector_database.test_connection()

    def list_collections(self) -> list[str]:
        return self.vector_database.list_collections()

    def search_text(self, search: Search) -> list[str]:
        return self.vector_database.search_text(search)

    async def save(self, file_batch: FileBatch, collection_name: str):
        return await self.vector_database.insert_data(collection_name, file_batch)

    async def delete(self, collection: CollectionDto):
        return self.vector_database.delete_collection(collection)

    async def create_collection_schema(self,collection_schema: CollectionDto):
        return self.vector_database.create_collection_schema(collection_schema)

    async def check_if_collection_exists(self, collection_name: str):
        return self.vector_database.check_if_collection_exists(collection_name)
    
    async def delete_data_collection(self, collection: CollectionDto):
        return await self.vector_database.delete_data_collection(collection)

# Singleton and dependency injection
VectorDBServiceInstanceQdrant = VectorDBServiceQdrant(vector_database=QdrantInstance)