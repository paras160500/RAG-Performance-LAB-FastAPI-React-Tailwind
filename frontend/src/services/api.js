const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api"

async function request(endpoint , options = {}){
    const response = await fetch(`${API_URL}${endpoint}`,
    {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    }
  );
  if(!response.ok){
    let message = "Request failed."
    try{
        const error = await response.json()
        message = error.detail || message
    }
    catch{

    }
    throw new Error(message)
  }
  return response.json()
}


export function healthCheck() {
  return request("/health");
}


export function getDataset(datasetId) {
  return request(
    `/datasets/${datasetId}`
  );
}

export function searchVectors(data) {
  return request(
    "/retrieval/search",
    {
      method: "POST",
      body: JSON.stringify(data),
    }
  );
}

export async function runBenchmark(data) {
  const result = await request(
    "/benchmark/run",
    {
      method: "POST",
      body: JSON.stringify(data),
    }
  );

  console.log("🔥 BENCHMARK API RESPONSE:", result);

  return result;
}

export function getBenchmarkHistory() {
  return request(
    "/benchmark/history"
  );
}
