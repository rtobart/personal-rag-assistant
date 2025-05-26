from app.models.file import FileBatch
from app.services.notion_service import NotionService
from app.services.query_processing import process_query
from app.services.vector_db_service_qdrant import VectorDBServiceInstanceQdrant, VectorDBServiceQdrant


class BulkContentService:
    def __init__(self,
                 notion_service: NotionService):
        self.notion_service = notion_service
        self.vector_db_service = VectorDBServiceInstanceQdrant

    async def bulk_insert(self, collection_name: str, embedding_algorithm: str):
        """
        Bulk insert content from Notion to Qdrant.
        """
        # Get blocks from Notion
        blocks = await self.notion_service.get_blocks_children()
        print('blocks: ', blocks)

        # Prepare data for Qdrant
        query = {
            "query": blocks,
            "embedding": embedding_algorithm
        }
        chunks = await process_query(query)
        files = FileBatch(
            file_chunks=chunks,
            collection_name=collection_name
        )

        # Insert data into Qdrant
        await self.vector_db_service.insert_data(collection_name, files)
        return {"status": "success", "message": f"Data inserted into {collection_name}."}
