from typing import Any 
from app.db.supabase import get_supabase_client

class DatabaseService:
    def __init__(self):
        self.client = get_supabase_client()

    def get_dataset(self , dataset_id : str) -> dict[str , Any]:
        response = (
            self.client.table("datasets").select("*").eq("id" , dataset_id).single().execute()
        )
        return response.data 

    def create_query(self , dataset_id : str , seed : int , dimension : int) -> dict[str , Any]:
        response = (self.client.table("queries").insert(
            {
                "dataset_id" : dataset_id,
                "seed" : seed,
                "dimension" : dimension
            }
        ).execute())
        return response.data[0]

    def save_benchmark(self , query_id : str , results : list[dict] , speedup : float) -> list[dict]:
        rows = []
        for result in results:
            rows.append(
                {
                    "query_id" : query_id,
                    "algorithm" : result['algorithm'],
                    "iterations" : result['iterations'],
                    "total_time_ms" : result['total_time_ms'],
                    "average_latency_ms" : result['average_latency_ms'],
                    "min_latency_ms" : result['min_latency_ms'],
                    "max_latency_ms" : result['max_latency_ms'],
                    "queries_per_second" : result['queries_per_second'],
                    "speedup" : (speedup if result['algorithm'] == "faiss" else None)
                }
            )

            response = (
                self.client.table("benchmark_runs").insert(rows).execute()
            )

            return response.data 