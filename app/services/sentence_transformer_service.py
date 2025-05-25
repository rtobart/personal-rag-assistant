import httpx
from app.logger.logger import LoggerInstance

class SentenceTransformerService:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        try:
            LoggerInstance.info("Requesting embeddings from SentenceTransformer API")
            response = await self.client.post(
                f"{self.base_url}/encode",
                json={"texts": texts},
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            return result["embeddings"]  # Extraer la clave 'embeddings'
        except Exception as e:
            LoggerInstance.error(f"Failed to fetch embeddings: {str(e)}")
            raise

def get_sentence_transformer_service() -> SentenceTransformerService:
    return SentenceTransformerService()