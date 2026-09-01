import time 
from app.services.retrieval_service import RetrievalService
import numpy as np

class BenchmarkService:
    def __init__(self , retrieval_service : RetrievalService):
        self.retrieval_service = retrieval_service

    def benchmark(self , query_vector : list[float] , top_k : int , iterations : int) -> list[dict]:
        query_vector = np.asarray(query_vector, dtype=np.float32)
        results = []
        algorithms = ["numpy" , "faiss"]

        for algorithm in algorithms:
            latencies = []
            self.retrieval_service.search(query_vector , algorithm , top_k)
            for _ in range(iterations):
                start = time.perf_counter()
                self.retrieval_service.search(query_vector , algorithm , top_k)
                end = time.perf_counter()
                latency_ms = (end - start) * 1000 
                latencies.append(latency_ms)
            total_time_ms = sum(latencies)
            average_latency_ms = total_time_ms / iterations
            min_latency_ms = min(latencies)
            max_latency_ms = max(latencies)
            total_seconds = total_time_ms / 1000 
            queries_per_second = (iterations / total_seconds if total_seconds > 0 else 0)
            results.append(
                {
                    "algorithm" : algorithm,
                    "iterations" : iterations,
                    "total_time_ms" : round(total_time_ms , 4),
                    "average_latency_ms" : round(average_latency_ms , 4),
                    "min_latency_ms" : round(min_latency_ms , 4),
                    "max_latency_ms" : round(max_latency_ms , 4),
                    "queries_per_second" : round(queries_per_second , 4)
                }
            )

        return results