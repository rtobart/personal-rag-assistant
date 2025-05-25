# Third party libraries
from llama_index.core.node_parser import SentenceSplitter

# Native libraries
import asyncio
import os
import tempfile

# Project libraries
from app.config.config import VARS
from app.config.config_instance import ConfigInstance
from app.logger.logger import Logger, LoggerInstance
from app.models.data_processing_model import Document


class DataProcessor:
    """
    Data Processing Class.
    """

    def __init__(self, logger: Logger):
        self.logger = logger

    async def get_direct_chunks(self, text: str, chunk_size: int = ConfigInstance.get(VARS.DEFAULT_CHUNK_SIZE.value),
                                chunk_overlap: int = ConfigInstance.get(VARS.DEFAULT_CHUNK_OVERLAP_SIZE.value),
                                metadata: dict = {}) -> list[Document]:
        """
        Obtain chunks directly from text, without doing DISK I/O.

        Parameters:
        text (str): The text to split into chunks.
        chunk_size (int): The size of each chunk.
        chunk_overlap (int): The overlap size between chunks.
        metadata (dict): Metadata to include with each chunk.

        Returns:
        list[Document]: A list of Document objects containing chunks of the text.
        """
        try:
            self.text_splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

            loop = asyncio.get_event_loop()

            def build_custom_chunk(text: str) -> Document:
                return Document(text=text, metadata=metadata)

            chunks = await loop.run_in_executor(None, lambda: self.text_splitter.split_text(text))
            chunks: list[Document] = list(map(build_custom_chunk, chunks))

            return chunks
        except Exception as e:
            self.logger.critical("ERROR TRYING TO GET CHUNKS FROM TEXT PLAIN EXTRACTION")
            self.logger.error(str(e))
            raise e


DataProcessorInstance = DataProcessor(logger=LoggerInstance)