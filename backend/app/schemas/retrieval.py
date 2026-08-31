from pydantic import BaseModel, Field

class RetrievalRequest(BaseModel):
    """
        Request body for vector retrieval
    """
    query_vector : list[float] = Field(
        ...,
        description = "Embedding vector representing the user's query",
        min_length=1
    )
    document_vectors : list[list[float]] = Field(
        ...,
        description="Collection of document embedding vectors.",
        min_length=1
    )
    top_k : int = Field(
        default = 5,
        ge = 1,
        description = "Number of most similar documents to retrieve."
    )


class RetrievalResult(BaseModel):
    """
        Single retrieval result
    """
    index : int 
    similarity : float 


class RetrievalResponse(BaseModel):
    """
        Response returned by the retrieval API.
    """
    algorithm : str 
    top_k : int 
    results : list[RetrievalResult]