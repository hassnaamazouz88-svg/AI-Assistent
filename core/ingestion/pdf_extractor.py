import fitz

from core.ingestion.ocr_extractor import ocr_page_with_pennyocr


def is_page_scanned(page: fitz.Page, seuil_caracteres: int = 20) -> bool:
    texte = page.get_text().strip()
    return len(texte) < seuil_caracteres


def extract_pdf(file_path: str) -> dict:
    """
    Extrait le texte d'un fichier PDF, page par page.
    Les pages scannées passent par l'OCR (PennyOCR).
    """
    pages = []
    full_text = []
    scanned_pages = 0

    with fitz.open(file_path) as document:

        for page_number, page in enumerate(document, start=1):

            text = page.get_text("text").strip()
            is_scanned = is_page_scanned(page)

            if is_scanned:
                scanned_pages += 1
                text = ocr_page_with_pennyocr(page)

            pages.append({
                "page_number": page_number,
                "text": text,
                "is_scanned": is_scanned
            })

            if text:
                full_text.append(text)

    return {
        "text": "\n\n".join(full_text),
        "pages": pages,
        "total_pages": len(pages),
        "scanned_pages": scanned_pages
    }