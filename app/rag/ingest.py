from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


def main():
    # Load embedding model
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    # Create ChromaDB client
    chroma_path = Path("app/rag/chroma_db")
    client = chromadb.PersistentClient(path=str(chroma_path))

    # Create or get collection
    collection = client.get_or_create_collection(
        name="financial_risk_policies"
    )

    # Read policy document
    document_path = Path("app/rag/documents/risk_policy.txt")
    document_text = document_path.read_text(encoding="utf-8")

    # Create embedding
    embedding = embedding_model.encode(document_text).tolist()

    # Store document in ChromaDB
    collection.upsert(
        ids=["risk_policy_001"],
        documents=[document_text],
        embeddings=[embedding],
        metadatas=[
            {
                "source": "risk_policy.txt",
                "document_type": "financial_risk_policy",
            }
        ],
    )

    print("\n--- RAG Ingestion ---")
    print("Policy document ingested successfully!")
    print(f"Collection: {collection.name}")
    print(f"Documents stored: {collection.count()}")


if __name__ == "__main__":
    main()