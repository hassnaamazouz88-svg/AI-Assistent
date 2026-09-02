from pathlib import Path

from core.ingestion.file_detector import detect_file_type

from core.ingestion.pdf_extractor import extract_pdf
from core.ingestion.docx_extractor import extract_docx
from core.ingestion.xlsx_extractor import extract_xlsx
from core.ingestion.doc_converter import convert_doc_to_docx

from core.ingestion.text_builder import (
    build_text_from_pdf,
    build_text_from_docx,
    build_text_from_xlsx,
)


def process_document(file_path: str) -> str:
    """
    Point d'entrée unique du pipeline d'ingestion.

    Cette fonction :
        1. Détecte le type du fichier
        2. Appelle l'extracteur approprié
        3. Construit le texte final
        4. Retourne le texte prêt pour le chunking

    Formats actuellement pris en charge :
        - PDF
        - DOCX
        - DOC
        - XLSX

    Args:
        file_path: chemin du fichier à traiter

    Returns:
        str: texte final extrait du document
    """

    # Vérification de l'existence du fichier
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {file_path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Le chemin indiqué n'est pas un fichier : {file_path}"
        )

    # ---------------------------------------------------------
    # 1. Détection du type
    # ---------------------------------------------------------

    document_type = detect_file_type(file_path)

    # ---------------------------------------------------------
    # 2. Traitement du PDF
    # ---------------------------------------------------------

    if document_type == "pdf":

        extracted_data = extract_pdf(file_path)

        return build_text_from_pdf(extracted_data)

    # ---------------------------------------------------------
    # 3. Traitement du DOCX
    # ---------------------------------------------------------

    elif document_type == "docx":

        extracted_data = extract_docx(file_path)

        return build_text_from_docx(extracted_data)

    # ---------------------------------------------------------
    # 4. Traitement du DOC
    # ---------------------------------------------------------

    elif document_type == "doc":

        # Conversion DOC → DOCX
        docx_path = convert_doc_to_docx(file_path)

        # Extraction du DOCX obtenu
        extracted_data = extract_docx(docx_path)

        # Construction du texte final
        return build_text_from_docx(extracted_data)

    # ---------------------------------------------------------
    # 5. Traitement du XLSX
    # ---------------------------------------------------------

    elif document_type == "xlsx":

        extracted_data = extract_xlsx(file_path)

        return build_text_from_xlsx(extracted_data)

    # ---------------------------------------------------------
    # 6. XLS non encore supporté
    # ---------------------------------------------------------

    elif document_type == "xls":

        raise NotImplementedError(
            "Le format .xls est détecté mais son extraction "
            "n'est pas encore implémentée."
        )

    # ---------------------------------------------------------
    # 7. Sécurité
    # ---------------------------------------------------------

    else:

        raise ValueError(
            f"Type de document non pris en charge : {document_type}"
        )