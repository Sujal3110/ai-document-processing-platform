import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str) -> dict:
    """Extract key fields from OCR'd document text."""
    doc = nlp(text)

    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    money = [ent.text for ent in doc.ents if ent.label_ == "MONEY"]

    # Invoice number: look for pattern like "INV-2026-00457"
    invoice_match = re.search(r"\b([A-Z]{2,4}-\d{4}-\d{4,6})\b", text)
    if not invoice_match:
        invoice_match = re.search(r"(?:Invoice|Inv)[\s#:]*([A-Z0-9\-]{5,})", text, re.IGNORECASE)
    invoice_number = invoice_match.group(1) if invoice_match else None

    # Total: pick the LAST money-like number in the text (usually the grand total)
    all_amounts = re.findall(r"[\d]{1,3}(?:,\d{2,3})*\.\d{2}", text)
    total_amount = all_amounts[-1] if all_amounts else (money[0] if money else None)

    return {
        "invoice_number": invoice_number,
        "total_amount": total_amount,
        "dates_found": dates,
        "vendor_candidates": orgs,
    }

if __name__ == "__main__":
    import sys
    sys.path.append("src/processing")
    from ocr_extract import process_document

    text = process_document("data/sample_docs/invoice1.png")
    entities = extract_entities(text)
    print(entities)