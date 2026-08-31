from pathlib import Path 
import numpy as np 

def generate_embeddings(number_of_vectors : int , dimension : int , seed : int = 42) -> np.ndarray:
    """
        Generate deterministic random embeddings for benchmarking 
        and developing
    """

    if number_of_vectors <= 0:
        raise ValueError("number_of_vectors must be greate than 0")
    if dimension <= 0:
        raise ValueError("dimension must be greate than 0")

    rng = np.random.default_rng(seed)
    embeddings = rng.normal(size=(number_of_vectors , dimension)).astype(np.float32)
    return embeddings

def save_embeddings(embeddings : np.ndarray , path : str) -> None:
    """
        Save embeddings as numpy .npy file
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True , exist_ok=True)
    np.save(file_path , embeddings)

def load_embeddings(path : str) -> np.ndarray:
    """
        Load embeddings from a numpy .npy file
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Embeddin dataset not dound : {file_path}")
    return np.load(file_path)