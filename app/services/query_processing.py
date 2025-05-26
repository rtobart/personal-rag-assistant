""" This module contains the functions to process a query. """

from ast import List
from app.logger.logger import LoggerInstance as logger
from app.models.file import FileChunk
from app.services.data_processing import DataProcessorInstance
from app.services.embeddings_service import use_embedding
from app.util.prepare_to_insert import prepare_event


async def process_query(query):
    print('query: ', query)
    """
    Process a query and return the embedding.

    Parameters:
    query (str): The query to process.

    Returns:
    dict: The embedding of the query.
    """
    try:
        logger.info("Processing query")
        embedding_service_instance = use_embedding.get(query["embedding"])
        text_blocks_length = len(query["query"])
        chunks_data: List[FileChunk] = []
        if text_blocks_length == 1:
            query["query"] = query["query"][0]
            query_length = len(query["query"])
            if query_length == 0:
                return

            if query_length > 400:
                document_chunks = await DataProcessorInstance.get_direct_chunks(
                    text=query["query"]
                )
                for document in document_chunks:
                    if hasattr(document, "text"):
                        chunks_data.append(
                            await prepare_event(document, embedding_service_instance)
                        )
                    else:
                        logger.error("Document chunk does not have 'text' attribute")
                return chunks_data

            chunk_size = query_length
            chunk_overlap = 0
            document = await DataProcessorInstance.get_direct_chunks(
                text=query["query"], chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )
            chunk_data = await prepare_event(document[0], embedding_service_instance)
            chunks_data.append(chunk_data)
        else:
            blocks = query["query"]
            for block in blocks:
                query_length = len(block)
                if query_length == 0:
                    continue

                if query_length > 400:
                    document_chunks = await DataProcessorInstance.get_direct_chunks(
                        text=block
                    )
                    for document in document_chunks:
                        if hasattr(document, "text"):
                            chunks_data.append(
                                await prepare_event(document, embedding_service_instance)
                            )
                        else:
                            logger.error("Document chunk does not have 'text' attribute")
                    continue
                chunk_size = query_length
                chunk_overlap = 0
                document = await DataProcessorInstance.get_direct_chunks(
                    text=block, chunk_size=chunk_size, chunk_overlap=chunk_overlap
                )
                chunk_data = await prepare_event(document[0], embedding_service_instance)
                chunks_data.append(chunk_data)
        return chunks_data
            
    except Exception as e:
        logger.error(str(e))
        raise e
