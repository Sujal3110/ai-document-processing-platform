import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model (downloads once, then cached locally)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Persistent ChromaDB client — data saved to disk, survives restarts
client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_or_create_collection(name="documents")

def add_document_to_store(doc_id: str, text: str, metadata: dict):
    """Generate embedding for document text and store in ChromaDB."""
    embedding = model.encode(text).tolist()
    collection.add(
        ids=[doc_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata]
    )
    print(f"Added '{doc_id}' to vector store.")

def search_documents(query: str, n_results: int = 3):
    """Search stored documents using natural language query."""
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results

if __name__ == "__main__":
    # Quick test
    add_document_to_store(
        doc_id="test1",
        text="This is an invoice for office chairs and laptops from Global Tech Supplies.",
        metadata={"type": "invoice", "vendor": "Global Tech Supplies"}
    )

    results = search_documents("office furniture purchase")
    print("\nSearch results:")
    print(results)