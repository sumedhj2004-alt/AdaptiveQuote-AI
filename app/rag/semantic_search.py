from pathlib import Path
import chromadb


# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Absolute path to ChromaDB
CHROMA_PATH = PROJECT_ROOT / "app" / "rag" / "chroma_db"


def search_policy(query, n_results=1):

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    collection = client.get_collection(
        name="financial_risk_policies"
    )

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results["documents"][0]

    return documents


if __name__ == "__main__":

    query = "What happens when a quotation has high financial risk?"

    results = search_policy(query)

    print("\n--- RAG Search Results ---")

    for document in results:
        print(document)