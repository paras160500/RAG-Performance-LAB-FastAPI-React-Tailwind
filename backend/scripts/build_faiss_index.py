from app.retrieval.faiss_engine import FAISSRetrievalEngine
from app.services.dataset_service import load_embeddings
EMBEDDINGS_PATH = "data/embeddings/embeddings_10k_1536.npy"
INDEX_PATH = "data/indexes/faiss_10k_1536.index"

def main():
    print("Loading embeddings....")
    embeddings = load_embeddings(EMBEDDINGS_PATH)
    print(f"Loading datasets : {embeddings.shape}")
    print("Building FAISS index...")
    engine = FAISSRetrievalEngine()
    engine.build_index(embeddings)
    print(f"FAISS index contains {engine.index.ntotal :,} vectors")
    print("Saving index...")
    engine.save(INDEX_PATH)
    print(F"Index saved to : {INDEX_PATH}")

if __name__ == "__main__":
    main()