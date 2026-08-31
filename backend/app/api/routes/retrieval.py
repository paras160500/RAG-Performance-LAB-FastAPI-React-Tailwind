import numpy as np
from fastapi import APIRouter, HTTPException
from app.retrieval.numpy_engine import retrieve_top_k
from app.schemas.retrieval import RetrievalResult , RetrievalResponse , RetrievalRequest

router = APIRouter(
    prefix="/retrieval",
    tags = ["Retrieval"]
)

@router.post("/search" , response_model=RetrievalResponse)
async def search_vectors(request : RetrievalRequest):
    """
        Search docment vectors using cosine similarity
    """
    try:
        query_vector = np.asarray(
            request.query_vector,
            dtype=np.float32
        )
        document_vectors = np.asarray(
            request.document_vectors, dtype=np.float32
        )
        results = retrieve_top_k(query_vector=query_vector , documents_vector=document_vectors , top_k=request.top_k)
        return RetrievalResponse(
            algorithm="numpy",
            top_k=request.top_k,
            results=results
        )
    except ValueError as exc:
        raise HTTPException(status_code=400 , detail=str(exc)) from exc 