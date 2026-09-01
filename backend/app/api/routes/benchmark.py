from fastapi import APIRouter,HTTPException
from app.schemas.benchmark import BenchMarkRequest , BenchmarkResponse
from app.services.benchmark_service import BenchmarkService
from app.services.container import retrieval_service

router = APIRouter(
    prefix="/benchmark",
    tags = ["Benchmark"]
)

benchmark_service = BenchmarkService(retrieval_service)

@router.post("/run" , response_model=BenchmarkResponse)
async def run_benchmark(request : BenchMarkRequest):
    try:
        results , speedup = benchmark_service.benchmark(
            query_vector=request.query_vector,
            top_k=request.top_k,
            iterations=request.iteration
        )
        return BenchmarkResponse(
            top_k=request.top_k,
            results=results,
            speedup=speedup
        )
    except(ValueError , RuntimeError) as exc:
        raise HTTPException(status_code=400 , detail=str(exc)) from exc