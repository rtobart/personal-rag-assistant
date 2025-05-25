import vertexai
from vertexai.language_models import TextEmbeddingModel
from app.config.config import VARS
from app.config.config_instance import ConfigInstance

GCLOUD_PROJECT = ConfigInstance.get("GCP_VERTEX_PROJECT_ID")
GCLOUD_REGION = ConfigInstance.get("GCP_VERTEX_LOCATION")
vertexai.init(project=GCLOUD_PROJECT, location=GCLOUD_REGION)

def get_embeddings(text: str, embedding_model: str) -> dict:
    try:
        model = TextEmbeddingModel.from_pretrained(embedding_model)
        return model.get_embeddings([text])
    except Exception as e:
        raise e
