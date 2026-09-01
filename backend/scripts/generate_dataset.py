from app.services.dataset_service import generate_embeddings , save_embeddings

NUMBER_OF_VECTORS = 10_000
EMBEDDING_DIMENSION = 1536

OUTPUT_PATH = ("data/embeddings/embeddings_10k_1536.npy")

def main():
    print(f"Generating {NUMBER_OF_VECTORS}")
    print(f"Vector with dimension : {EMBEDDING_DIMENSION}")

    embeddings = generate_embeddings(
        number_of_vectors= NUMBER_OF_VECTORS,
        dimension=EMBEDDING_DIMENSION
    )

    save_embeddings(embeddings=embeddings , path = OUTPUT_PATH)
    print(f"Saved Embeddings to : {OUTPUT_PATH}")
    print(f"Shape : {embeddings.shape}")
    print(f"Memory : {embeddings.nbytes / (1024 ** 2):.2f} MB")


if __name__ == "__main__":
    main()