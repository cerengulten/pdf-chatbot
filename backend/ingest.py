import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer 
import numpy as np 
import faiss
from pathlib import Path
import pickle


MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# Extract pages of PDF as text 
def extract_pdf(pdf_path: str) -> str:
  doc = fitz.open(pdf_path)
  return "\n".join(page.get_text() for page in doc)

# Getting text and splitting into smaller chunks for better processing and embedding 
def text_split(text:str)-> list[str]:
  splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
  )
  return splitter.split_text(text)

def embedding_chunks(chunks: list[str]) -> np.ndarray:
  return MODEL.encode(chunks, show_progress_bar=True)

def build_index(pdf_path: str, index_dir: str = "data/index"):
    Path(index_dir).mkdir(parents=True, exist_ok=True)

    text = extract_pdf(pdf_path)
    chunks = text_split(text)
    embeddings = embedding_chunks(chunks)

    # Build FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index and chunks side by side
    faiss.write_index(index, f"{index_dir}/index.faiss")
    with open(f"{index_dir}/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print(f"Done. {len(chunks)} chunks indexed.")
    return chunks, index