""" This module contains the functions to process a query. """

from typing import List
from app.logger.logger import LoggerInstance as logger
from app.models.file import FileChunk
from app.services.data_processing import DataProcessorInstance
from app.services.embeddings_service import use_embedding
from app.util.prepare_to_insert import prepare_event


async def _process_text_block(text: str, embedding_service_instance) -> List[FileChunk]:
    """
    Process a single text block and return chunks.
    
    Parameters:
    text (str): The text block to process.
    embedding_service_instance: The embedding service instance.
    
    Returns:
    List[FileChunk]: List of processed chunks.
    """
    if not text or len(text) == 0:
        return []

    chunks_data = []
    text_length = len(text)

    if text_length > 400:
        # For long texts, use default chunking
        document_chunks = await DataProcessorInstance.get_direct_chunks(text=text)
        for document in document_chunks:
            if hasattr(document, "text"):
                chunks_data.append(
                    await prepare_event(document, embedding_service_instance)
                )
            else:
                logger.error("Document chunk does not have 'text' attribute")
    else:
        # For short texts, use text length as chunk size
        document = await DataProcessorInstance.get_direct_chunks(
            text=text, chunk_size=text_length, chunk_overlap=0
        )
        if document:
            chunk_data = await prepare_event(document[0], embedding_service_instance)
            chunks_data.append(chunk_data)

    return chunks_data


async def process_query(query):
    """
    Process a query and return the embedding.

    Parameters:
    query (dict): The query to process containing 'query' and 'embedding' keys.

    Returns:
    List[FileChunk]: The processed chunks of the query.
    """
    try:
        logger.info("Processing query")
        embedding_service_instance = use_embedding.get(query["embedding"])
        query_blocks = query["query"]

        # Ensure query_blocks is always a list
        if not isinstance(query_blocks, list):
            query_blocks = [query_blocks]

        chunks_data: List[FileChunk] = []

        # Process each text block
        for block in query_blocks:
            block_chunks = await _process_text_block(block, embedding_service_instance)
            chunks_data.extend(block_chunks)

        return chunks_data

    except Exception as e:
        logger.error(str(e))
        raise e
