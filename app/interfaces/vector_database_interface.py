from abc import abstractmethod, ABC
from app.models.file import FileBatch
from app.models.search import Search

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
    def test_connection(self):
        """
            Test if the database is connected.
        """
        return self.online()

    @abstractmethod
    async def insert_data(self, collection_name: str, files: FileBatch):
        """
            Insert data into the engine.
        """
        pass

    @abstractmethod
    async def  search_text(self, search: Search):
        """
            search by text in collection.
        """
        pass
    
    @abstractmethod
    async def  search_text_filter(self, search: Search):
        """
            search by text in collection.
        """
        pass
    
    @abstractmethod
    async def  search_text_no_filter(self, search: Search):
        """
            search by text in collection.
        """
        pass
