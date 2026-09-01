from fastapi import APIRouter,HTTPException
from app.services.database_service import DatabaseService

router = APIRouter(
    prefix="/datasets",
    tags = ["Datasets"]
)

@router.get("/{dataset_id}")
async def get_dataset(dataset_id : str):
    try:
        service = DatabaseService()
        dataset = service.get_dataset(dataset_id)
        return dataset
    except Exception as exc:
        raise HTTPException(status_code=500 , detail = str(exc)) from exc