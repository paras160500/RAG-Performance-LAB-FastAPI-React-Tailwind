from app.core.config import settings
from app.services.retrieval_service import RetrievalService

retrieval_service = RetrievalService(
    embeddings_path=settings.EMBEDDINGS_PATH,
    faiss_index_path=settings.FAISS_INDEX_PATH
)