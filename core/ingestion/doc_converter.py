import subprocess
import os


def convert_doc_to_docx(file_path: str) -> str:
    """
    Convertit un fichier .doc (ancien format Word) en .docx,
    via LibreOffice en ligne de commande.

    Le fichier converti est créé dans le même dossier que
    le fichier d'origine.

    Args:
        file_path: chemin du fichier .doc à convertir

    Returns:
        Le chemin du fichier .docx généré.
    """
    output_dir = os.path.dirname(file_path)

    subprocess.run(
        [
            "soffice",
            "--headless",
            "--convert-to", "docx",
            "--outdir", output_dir,
            file_path
        ],
        check=True,
        timeout=60
    )

    # LibreOffice génère le fichier avec le même nom, extension .docx
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    docx_path = os.path.join(output_dir, f"{base_name}.docx")

    return docx_path