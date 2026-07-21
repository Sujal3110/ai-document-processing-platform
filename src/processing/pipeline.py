import json
from pathlib import Path
import sys

sys.path.append("src/processing")
from ocr_extract import process_document
from entity_extract import extract_entities
from embeddings import add_document_to_store, search_documents

def run_pipeline(file_path: str) -> dict:
    raw_text = process_document(file_path)
    entities = extract_entities(raw_text)

    doc_id = Path(file_path).stem  # e.g. "invoice1"
    metadata = {
        "file_name": Path(file_path).name,
        "invoice_number": str(entities.get("invoice_number") or "unknown"),
        "total_amount": str(entities.get("total_amount") or "unknown"),
    }

    # Store in vector DB for semantic search
    add_document_to_store(doc_id=doc_id, text=raw_text, metadata=metadata)

    return {
        "file_name": Path(file_path).name,
        "raw_text": raw_text,
        "extracted_entities": entities,
    }

if __name__ == "__main__":
    import glob
    results = []
    for file in glob.glob("data/sample_docs/*"):
        print(f"Processing: {file}")
        result = run_pipeline(file)
        results.append(result)

    with open("data/processed_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nDone. {len(results)} documents processed and embedded.")

    # Quick semantic search test
    print("\n--- Test Search ---")
    search_results = search_documents("laptop and office equipment invoice")
    for doc, meta, dist in zip(
        search_results["documents"][0],
        search_results["metadatas"][0],
        search_results["distances"][0]
    ):
        print(f"\nMatch (distance={dist:.3f}): {meta}")