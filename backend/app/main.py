from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.retrieval import router as retrieval_router

app = FastAPI(
    title = "RAG Performance LAB",
    description = "Backend API for RAG Lab",
    version = "0.1.0"
)

app.include_router(health_router , prefix = "/api")
app.include_router(retrieval_router , prefix="/api")

@app.get("/")
async def root():
    return {
        "message" : "RAG Performance LAB",
        "version" : "0.1.0",
        "status" : "running"
    }