import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(question: str, index_dir: str = "data/index", k: int = 3) -> list[str]:
    index = faiss.read_index(f"{index_dir}/index.faiss")
    with open(f"{index_dir}/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    vector = MODEL.encode([question])
    _, indices = index.search(np.array(vector), k=k)
    return [chunks[i] for i in indices[0] if i < len(chunks)]