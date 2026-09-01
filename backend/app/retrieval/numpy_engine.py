import numpy as np 
from app.retrieval.cosine import cosine_similairy

def retrieve_top_k(query_vector: np.ndarray,documents_vector: np.ndarray,top_k: int = 5):
    query_vector = np.asarray(query_vector, dtype=np.float32)
    documents_vector = np.asarray(documents_vector,dtype=np.float32)
    if query_vector.ndim != 1:
        raise ValueError("query_vector must be a 1D vector")

    if documents_vector.ndim != 2:
        raise ValueError("documents_vector must be a 2D array")

    if query_vector.size == 0:
        raise ValueError("query_vector cannot be empty")

    if documents_vector.shape[0] == 0:
        raise ValueError("documents_vector cannot be empty")

    if documents_vector.shape[1] != query_vector.shape[0]:
        raise ValueError(
            "query_vector and documents_vector must have the same dimensions"
        )

    top_k = min(top_k, documents_vector.shape[0])

    query_norm = np.linalg.norm(query_vector)
    document_norms = np.linalg.norm(documents_vector, axis=1)

    if query_norm == 0:
        raise ValueError("query_vector cannot be a zero vector")

    if np.any(document_norms == 0):
        raise ValueError("document vectors cannot contain zero vectors")

    similarities = (
        documents_vector @ query_vector
    ) / (document_norms * query_norm)

    top_indices = np.argsort(similarities)[::-1][:top_k]

    return [
        {
            "index": int(index),
            "similarity": float(similarities[index]),
        }
        for index in top_indices
    ]