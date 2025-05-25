""" This module contains the functions to process a query. """

from app.logger.logger import LoggerInstance as logger
from app.services.data_processing import DataProcessorInstance
from app.services.embeddings_service import use_embedding
from app.util.prepare_to_insert import prepare_event


async def process_query(query):
    """
    Process a query and return the embedding.

    Parameters:
    query (str): The query to process.

    Returns:
    dict: The embedding of the query.
    """
    try:
        logger.info("Processing query")
        embedding_algorithm = use_embedding.get(query["embedding"])
        query_length = len(query["query"])
        if query_length == 0:
            return

        if query_length > 400:
            document_chunks = await DataProcessorInstance.get_direct_chunks(
                text=query["query"]
            )
            chunk_data = []
            for document in document_chunks:
                if hasattr(document, "text"):
                    chunk_data.append(
                        await prepare_event(document, embedding_algorithm)
                    )
                else:
                    logger.error("Document chunk does not have 'text' attribute")
            return chunk_data

        chunk_size = query_length
        chunk_overlap = 0
        document = await DataProcessorInstance.get_direct_chunks(
            text=query["query"], chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        print(document)
        chunk_data = await prepare_event(document[0], embedding_algorithm)
        return chunk_data
    except Exception as e:
        logger.error(str(e))
        raise e
