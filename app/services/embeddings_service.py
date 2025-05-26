# Third party libraries
import httpx

# Project libraries
from app.config import config_instance
from app.config.config import VARS
# from app.exceptions.exceptions import EmbeddingException
from app.logger.logger import LoggerInstance
from app.services.sentence_transformer_service import get_sentence_transformer_service


class EmbeddingProcess:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.client = httpx.AsyncClient()
class TextEmbedding:
    def __init__(self, values, statistics):
        self.values = values
        self.statistics = statistics

sentence_transformer_service = get_sentence_transformer_service()

class SentenceTransformerEmbedding(EmbeddingProcess):
    def __init__(self):
        super().__init__(model_name="sentence-transformer")

    async def create(self, text: str) -> list[float]:
        embeddings = await sentence_transformer_service.get_embeddings([text])
        return embeddings[0]

class GcloudEmbeddingModel(EmbeddingProcess):
    def __init__(self, model_name: str = "text-multilingual-embedding-002"):
        super().__init__(model_name)

    async def create(self, text: str) -> list[float]:
        """
        Return a 768 dimensional vector of floating point numbers.

        Parameters:
        text (str): The text to be embedded.

        Returns:
        list[float]: The embedding of the text.
        """
        try:
            LoggerInstance.info("Init embeddings")
            # response = get_embeddings(text, self.model_name)
            response = "" #TODO: Remove this line when the get_embeddings function is implemented
            embeddings = [embedding.values for embedding in response][0]
            if not all(isinstance(value, float) for value in embeddings):
                raise ValueError("Embedding values must be floats")
            return embeddings
        except Exception as e:
            print(e)
            LoggerInstance.error(str(e))

GCLOUD_EMBEDDING_MODEL = config_instance.ConfigInstance.get("GCLOUD_EMBEDDING_MODEL")
gcloudEbedding = GcloudEmbeddingModel(GCLOUD_EMBEDDING_MODEL)
sentenceTransformerEmbedding = SentenceTransformerEmbedding()
use_embedding = {
    "vertex": gcloudEbedding,
    "sentence-transformer": sentenceTransformerEmbedding,
}
