from fastapi import APIRouter,HTTPException
from app.schemas.benchmark import BenchMarkRequest , BenchmarkResponse, AlgorithmBenchmark
from app.services.benchmark_service import BenchmarkService
from app.services.container import retrieval_service
from app.services.database_service import DatabaseService

router = APIRouter(
    prefix="/benchmark",
    tags = ["Benchmark"]
)

benchmark_service = BenchmarkService(retrieval_service)

DATASET_ID = "c56d587d-3f95-4534-becb-0f203c1b629a"

@router.post("/run" , response_model=BenchmarkResponse)
async def run_benchmark(request : BenchMarkRequest):
    try:
        # Run benchmark
        results , speedup = benchmark_service.benchmark(
            query_vector=request.query_vector,
            top_k=request.top_k,
            iterations=request.iteration
        )
        # Supabase
        database = DatabaseService()
        # Save query metadata
        query = database.create_query(
            DATASET_ID , request.seed , len(request.query_vector)
        )
        # Save benchmark results
        database.save_benchmark(query['id'] , results , speedup)
        # Return API response 
        return BenchmarkResponse(
            query_id=query['id'],
            top_k=request.top_k,
            results=[
                AlgorithmBenchmark(**result) for result in results
            ],
            speedup=speedup
        )
    except(ValueError , RuntimeError) as exc:
        raise HTTPException(status_code=400 , detail=str(exc)) from exc

    except Exception as exc:
        raise HTTPException(500 , f"Failed to run and save banchmark :- {exc}") from exc


@router.get("/history")
async def benchmark_history(limit : int = 20):
    try:
        database = DatabaseService()
        return database.get_recent_benchmarks(limit)
    except Exception as e:
        raise HTTPException(500 , str(e)) from e 