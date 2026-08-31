import numpy as np 
from app.retrieval.cosine import cosine_similairy

def retrieve_top_k(query_vector : np.ndarray , documents_vector : np.ndarray , top_k : int = 5) -> list[dict]:
    """
        Retrieve the top-K most similarr documents
        Returns results order fro higherst similarity to lowest
    """

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")

    if top_k > len(documents_vector):
        top_k = len(documents_vector)

    similarities = cosine_similairy(query_vector=query_vector , document_vectors=documents_vector)

    # Get indices
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []

    for index in top_indices:
        results.append(
            {
                "index" : int(index),
                "similarity" : float(similarities[index])
            }
        )

    return results