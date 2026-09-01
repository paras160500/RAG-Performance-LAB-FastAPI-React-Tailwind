from pydantic import BaseModel , Field 

class BenchMarkRequest(BaseModel):
    query_vector : list[float] = Field(
        ... , min_length=1
    )
    top_k : int = Field(default = 5 , ge = 1)
    iteration : int = Field(default=10, ge=1,le=1000)

class AlgorithmBenchmark(BaseModel):
    algorithm : str 
    iterations : int 
    total_time_ms : float 
    average_latency_ms : float
    min_latency_ms : float 
    max_latency_ms: float 
    queries_per_second : float 

class BenchmarkResponse(BaseModel):
    top_k : int 
    results : list[AlgorithmBenchmark]
    speedup : float | None = None 