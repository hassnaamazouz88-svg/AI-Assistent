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

    Détecte le type du fichier, effectue l'extraction,
    puis construit le texte final prêt pour le chunking.
    """

    document_type = detect_file_type(file_path)

    if document_type == "pdf":

        extracted_data = extract_pdf(file_path)
        return build_text_from_pdf(extracted_data)

    elif document_type == "docx":

        extracted_data = extract_docx(file_path)
        return build_text_from_docx(extracted_data)

    elif document_type == "doc":

        docx_path = convert_doc_to_docx(file_path)
        extracted_data = extract_docx(docx_path)
        return build_text_from_docx(extracted_data)

    elif document_type == "xlsx":

        extracted_data = extract_xlsx(file_path)
        return build_text_from_xlsx(extracted_data)

    else:
        raise ValueError(
            f"Type de document non pris en charge : {document_type}"
        )