import numpy as np
from fastapi import APIRouter, HTTPException
from app.retrieval.numpy_engine import retrieve_top_k
from app.schemas.retrieval import RetrievalResult , RetrievalResponse , RetrievalRequest
from app.services.container import retrieval_service

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
        results = retrieval_service.search(
            request.query_vector,
            request.algorithm,
            request.top_k
        )
        return RetrievalResponse(
            algorithm=request.algorithm,
            top_k=request.top_k,
            results=results
        )
    except ValueError as exc:
        raise HTTPException(status_code=400 , detail=str(exc)) from exc 
    