import numpy as np 
from app.retrieval.faiss_engine import FAISSRetrievalEngine
from app.retrieval.numpy_engine import retrieve_top_k
from app.services.dataset_service import load_embeddings

class RetrievalService:
    """
        Central service resposible for loading the dataset
        and executing retrieval using different algorithms
    """
    def __init__(self , embeddings_path : str , faiss_index_path : str):
        self.embeddings_path = embeddings_path
        self.faiss_index_path = faiss_index_path
        self.embeddings:np.ndarray | None = None 
        self.faiss_engine : FAISSRetrievalEngine | None = None 

    def load(self) -> None:
        """
            Load the dataset and FAISS index
        """
        self.embeddings = load_embeddings(self.embeddings_path)
        self.faiss_engine = FAISSRetrievalEngine()
        self.faiss_engine.load(self.faiss_index_path)

    def search(self , query_vector : list[float] , algorithm : str , top_k : int) -> list[dict]:
        if self.embeddings is None:
            raise RuntimeError("Retrieval dataset has not been loaded")
        query = np.asarray(query_vector , dtype = np.float32)
        if algorithm == "numpy":
            return retrieve_top_k(query_vector , self.embeddings , top_k)
        if algorithm == "faiss":
            if self.faiss_engine is None:
                raise RuntimeError("FAISS Engine has not been loaded")
            return self.faiss_engine.search(query , top_k)
        raise ValueError(f"unsupported algo { algorithm}")