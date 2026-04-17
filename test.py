from backend.ingest import extract_pdf, text_split, embedding_chunks, build_index
import faiss, pickle, numpy as np

# 1. Build the index from any PDF you have
chunks, index = build_index("data/uploads/test.pdf")

# 2. Ask a question and find the top 3 matching chunks
question = "What is this document about?"
q_vector = embedding_chunks([question])
distances, indices = index.search(q_vector, k=3)

print("\n--- Top 3 relevant chunks ---")
for i, idx in enumerate(indices[0]):
    print(f"\n[{i+1}] {chunks[idx][:300]}")