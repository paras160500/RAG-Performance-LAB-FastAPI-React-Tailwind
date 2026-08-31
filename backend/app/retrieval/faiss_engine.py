from pathlib import Path
import faiss
import numpy as np 

class FAISSRetrievalEngine:
    """
        FAISS based vector retrieval engine.
        This will use indexflatI{ with normalized vectors,
        making inner product equivalent to cosinse similarity.
    """
    def __init__(self):
        self.index = None 
        self.dimension = None 

    def build_index(self , document_vectors : np.ndarray) -> None:
        """
            Build a FAISS index from document vectors.
            Args:
                document_vectors : shape:(number_of_documents , embedding_dimension)
        """
        vectors = self._prepare_vectors(document_vectors)
        self.dimension = vectors.shape[1]

        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(vectors)

    def search(self , query_vector : np.ndarray , top_k : int = 5) -> list[dict]:
        """
            Search the FAISS index.
            Returns the top-K documents with their
            similarity scores.
        """
        if self.index is None:
            raise RuntimeError("FAISS index has not been built")
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")
        if top_k > self.index.ntotal:
            top_k = self.index.ntotal
        query = self._prepare_query(query_vector)
        similarities , indices = self.index.search(query , top_k)
        results = []

        for similarity, index in zip(similarities[0],indices[0]):
            if index == -1:
                continue
            results.append(
                {
                    "index" : int(index),
                    "similarity" : float(similarity)
                }
            )
        return results

    def save(self , path : str) -> None:
        """
            Save the FAISS index to disk
        """
        if self.index is None:
            raise RuntimeError("Cannot save any empty FAISS index.")

        file_path = Path(path)
        file_path.parent.mkdir(parents = True , exist_ok=True)

        faiss.write_index(self.index , str(file_path))

    def load(self , path : str) -> None:
        """
            Loads the FAISS index from the disk
        """
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"FAISS index not found : {file_path}")

        self.index = faiss.read_index(str(file_path))
        self.dimension = self.index.d

    @staticmethod
    def _prepare_vectors(vectors : np.ndarray) -> np.ndarray:
        """
            Convert vectors to float32 and normalize them
        """
        vectors = np.asarray(
            vectors , dtype=np.float32
        )
        if vectors.ndim != 2:
            raise ValueError("document_vectors must be 2-dimensional.")
        if vectors.shape[0] == 0:
            raise ValueError("document_vectors cannot be empty.")

        faiss.normalize_L2(vectors)
        return vectors

    @staticmethod
    def _prepare_query(query_vector : np.ndarray) -> np.ndarray:
        """
            Convert the query vector into the 
            float32 -> reshape it and normalize it.
        """
        query = np.asarray(
            query_vector , dtype = np.float32
        )
        if query.ndim == 1:
            query = query.reshape(1,-1)
        if query.ndim != 2:
            raise ValueError("query_vector must be 1-dimention")

        faiss.normalize_L2(query)
        return query 