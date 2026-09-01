import fitz
import requests

from config.settings import settings

PENNYOCR_URL = "https://api.pennyocr.com/v1/ocr"


def ocr_page_with_pennyocr(page: fitz.Page, dpi: int = 250) -> str:
    """
    Effectue l'OCR d'une page PDF scannée via l'API PennyOCR.

    On envoie uniquement l'image de la page concernée (rasterisée en
    PNG), pas le PDF entier — pour ne payer que les pages réellement
    scannées, puisque PennyOCR facture à la page traitée.

    Les 100 premières pages sont gratuites (quota par compte, sans
    carte bancaire) — au-delà, l'API renvoie une erreur 402.

    Args:
        page: objet page PyMuPDF (fitz.Page)
        dpi: résolution de rasterisation avant OCR

    Returns:
        Le texte reconnu sur la page.
    """
    pixmap = page.get_pixmap(dpi=dpi)
    image_bytes = pixmap.tobytes("png")

    headers = {
        "Authorization": f"Bearer {settings.PENNYOCR_API_KEY}"
    }
    files = {
        "file": ("page.png", image_bytes, "image/png")
    }
    params = {
        "format": "text"
    }

    response = requests.post(
        PENNYOCR_URL,
        headers=headers,
        files=files,
        params=params,
        timeout=30
    )

    if response.status_code == 402:
        raise RuntimeError(
            "Quota PennyOCR épuisé (100 pages gratuites utilisées). "
            "Achète des crédits sur le dashboard pour continuer."
        )
    elif response.status_code != 200:
        raise RuntimeError(
            f"Erreur PennyOCR ({response.status_code}) : {response.text}"
        )

    data = response.json()
    return data["text"].strip()
