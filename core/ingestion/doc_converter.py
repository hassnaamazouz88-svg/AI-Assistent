import subprocess
import os


def convert_doc_to_docx(file_path: str) -> str:
    """
    Convertit un fichier .doc (ancien format Word) en .docx,
    via LibreOffice en ligne de commande.

    Utilise des chemins absolus pour éviter toute ambiguïté liée
    au répertoire de travail courant du processus qui exécute ce
    code (différent selon qu'on lance un script directement ou
    via le serveur Uvicorn).

    Args:
        file_path: chemin du fichier .doc à convertir

    Returns:
        Le chemin absolu du fichier .docx généré.
    """
    # Convertir en chemins absolus
    file_path = os.path.abspath(file_path)
    output_dir = os.path.dirname(file_path)

    result = subprocess.run(
        [
            "soffice",
            "--headless",
            "--convert-to", "docx",
            "--outdir", output_dir,
            file_path
        ],
        capture_output=True,
        text=True,
        timeout=60
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Échec de la conversion LibreOffice pour '{file_path}'.\n"
            f"Code retour : {result.returncode}\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    docx_path = os.path.join(output_dir, f"{base_name}.docx")

    return docx_path