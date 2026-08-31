import numpy as np 

def cosine_similairy(query_vector : np.ndarray , document_vectors : np.ndarray) -> np.ndarray:
    """
        Calculate cosine similairty between one query vector and 
        multiple document vectors.
        Args:
            query_vector : Shape: (dimensions , )
            document_vectors : Shape: (number_of_documents , dimensions)
        Returns:
            Similarity score for every document
    """
    # Check the query is 1 dim
    query_vector = np.asarray(query_vector , dtype=np.float32).reshape(-1)

    # Document vectors are 2 dim matrix
    document_vectors = np.asarray(
        document_vectors , dtype= np.float32
    )

    if document_vectors.ndim != 2:
        raise ValueError("document_vectors must be a 2-dimensional array")

    if query_vector.shape[0] != document_vectors.shape[1]:
        raise ValueError("Query vector dimension must match documnet vector dimensions")

    # Dot product btwn query and each document vector 
    dot_products = document_vectors @ query_vector

    # Calculate vector magnitudes.
    query_norm = np.linalg.norm(document_vectors , axis=1)

    # Prevent division by 0
    if query_norm == 0:
        raise ValueError("Query vector cant be a zero vector")

    # A.B / (||A|| ||B||)
    document_norms = np.where(
        document_norms == 0 , 1e-10 , document_norms
    )

    similarities = dot_products / (document_norms * query_norm)

    return similarities