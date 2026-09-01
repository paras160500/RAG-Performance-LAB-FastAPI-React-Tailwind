import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_ENV : str = os.getenv("APP_ENV" , "development")
    APP_NAME : str = os.getenv("APP_NAME" , "RAG PErformance LAB")
    APP_VERSION : str = os.getenv("APP_VERSION" , "0.1.0")
    EMBEDDINGS_PATH : str = os.getenv("EMBEDDINGS_PATH" , "data/embeddings/embeddings_10k_1536.npy")
    FAISS_INDEX_PATH : str = os.getenv("FAISS_INDEX_PATH" , "data/indexes/faiss_10k_1536.index")

settings = Settings()