# Third party libraries

# Project libraries
from app.logger.logger import LoggerInstance
from app.models.data_processing_model import Document
from app.models.file_incoming import FileChunk
from app.services.embeddings_service import EmbeddingProcess

logger = LoggerInstance


async def prepare_event(
    document: Document, embedding_process: EmbeddingProcess
) -> FileChunk:
    """
    Prepare serialized JSON to publish to EventHub.

    Parameters:
    document (Document): The document retrieved by langchain.
    collection (str): The collection to which the document belongs.
    embedding_process (EmbeddingProcess): The embedding process to use.

    Returns:
    dict: A dictionary containing the ready-to-publish event.
    """
    try:
        embedding = await embedding_process.create(text=document.text)
        data = FileChunk(
            metadata=document.metadata, content=document.text, embedding=embedding
        )
        return data.model_dump()
    except Exception as e:
        logger.error(f"Error preparing event: {e}")
        raise e
