from abc import abstractmethod, ABC
from app.models.collection import CollectionDto
from app.models.field import Field
from app.models.file import FileBatch

class VectorDatabaseInterface(ABC):
    """
        Generic vector database interface.
    """

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def online(self):
        """
        Verify that database connection is online.
        Otherwise, DatabaseOffline exception is raised.
        """
        pass

    @abstractmethod
    def prepare_data(self, files: FileBatch, dynamic_data: dict[str, list], **kwargs):
        """
            Prepare data to be inserted into db.
        """
        pass

    # PUBLIC METHODS
    @abstractmethod
    def test_connection(self):
        """
            Test if the database is connected.
        """
        return self.online()

    @abstractmethod
    def change_database(self, name):
        """
            Change using database to another one.
        """
        pass

    @abstractmethod
    def list_collections(self):
        """
            List all collections
        """
        pass

    @abstractmethod
    def create_field_schema(self, field: Field):
        """
            Create schema for a field.
        """
        pass

    @abstractmethod
    def create_collection_batch(self, collection: CollectionDto) -> CollectionDto:
        """
            Create collections.
        """
        pass

    @abstractmethod
    async def insert_data(self, collection_name: str, files: FileBatch):
        """
            Insert data into the engine.
        """
        pass

    @abstractmethod
    async def  check_if_collection_exists(self, collection_name: str):
        """
            Check if a collection exists.
        """
        pass
    
    @abstractmethod
    async def delete_data_collection(self, collection: CollectionDto):
        """
            Delete data from a collection.
        """
        pass
