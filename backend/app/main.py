from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.retrieval import router as retrieval_router
from contextlib import asynccontextmanager
from app.services.container import retrieval_service
from app.api.routes.benchmark import router as benchmark_router 
from app.api.routes.database import router as database_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Loading retrieval dataset...")
    retrieval_service.load()
    print("REtrieval dataset loaded.")
    yield
    print("shutting down...")

app = FastAPI(
    title = "RAG Performance LAB",
    description = "Backend API for RAG Lab",
    version = "0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
        allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://rag-performance-lab-fastapi-react.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router , prefix = "/api")
app.include_router(retrieval_router , prefix="/api")
app.include_router(benchmark_router , prefix="/api")
app.include_router(database_router , prefix="/api")

@app.get("/")
async def root():
    return {
        "message" : "RAG Performance LAB",
        "version" : "0.1.0",
        "status" : "running"
    }