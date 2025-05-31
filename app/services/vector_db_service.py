"""Service for interacting with the vector database."""
from app.interfaces.vector_database_interface import VectorDatabaseInterface
from app.models.file import FileBatch
from app.models.search import Search

class VectorDBService:
    """
    Service for interacting with the vector database.
    This service provides methods to test the connection, search text, and insert data.
    """
    def __init__(self, vector_database: VectorDatabaseInterface):
        self.vector_database = vector_database

    def test_connection(self):
        """
        Test if the database is connected.
        """
        return self.vector_database.test_connection()


    async def search_text(self, search: Search) -> list[str]:
        """
        Search by text in the collection.
        """
        return await self.vector_database.search_text(search)

    async def insert_data(self, collection_name: str, files: FileBatch):
        """
        Insert data into the vector database.
        :param collection_name: Name of the collection to insert data into.
        :param files: Batch of files to be inserted.
        :return: Result of the insert operation.
        """
        return await self.vector_database.insert_data(collection_name, files)

def get_vector_db_service(vector_database_instance: VectorDatabaseInterface) -> VectorDBService:
    """Returns an instance of VectorDBServiceQdrant, cached to avoid recreation."""
    return VectorDBService(vector_database=vector_database_instance)
