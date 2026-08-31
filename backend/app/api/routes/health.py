from datetime import datetime,timezone
from fastapi import APIRouter

router = APIRouter(
    tags=['Health']
)

@router.get("/health")
async def health_check():
    return {
        "status" : "Healthy",
        "service" : "RAG Performance LAB",
        "timestamp" : datetime.now(timezone.utc).isoformat()
    }
