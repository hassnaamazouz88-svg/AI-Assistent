import fitz


def is_page_scanned(page: "fitz.Page", seuil_caracteres: int = 20) -> bool:
    """
    Détermine si une page de PDF est scannée (image) ou native (texte réel).

    Une page est considérée comme scannée si l'extraction directe de son
    texte renvoie très peu de caractères, alors que la page contient
    visiblement du contenu.
    """
    texte = page.get_text().strip()
    return len(texte) < seuil_caracteres


def extract_pdf(file_path: str) -> dict:
    """
    Extrait le texte d'un fichier PDF, page par page.

    Retourne :
    {
        "text": "...",
        "pages": [
            {"page_number": 1, "text": "...", "is_scanned": False}
        ],
        "total_pages": 10,
        "scanned_pages": 2
    }

    Note : pour les pages détectées comme scannées, "text" reste vide
    à ce stade — leur contenu sera récupéré séparément via l'OCR
    (ocr_extractor.py), à une étape ultérieure du pipeline.
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