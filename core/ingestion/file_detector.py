from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".doc": "doc",
    ".xlsx": "xlsx",
    ".xls": "xls",
}


def detect_file_type(file_path: str) -> str:
    """
    Détecte le type d'un document à partir de son extension.

    Retourne :
        pdf, docx, doc, xlsx ou xls

    Lève :
        ValueError si le format n'est pas supporté.
    """
    extension = Path(file_path).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Format non supporté : {extension}"
        )

    return SUPPORTED_EXTENSIONS[extension]