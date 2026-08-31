import io
import os
import zipfile

from fastapi import UploadFile


def extract_zip_contents(
    zip_file: UploadFile,
    destination_dir: str
) -> list[str]:
    """
    Extrait le contenu d'un fichier ZIP dans destination_dir.

    Retourne la liste des chemins des fichiers extraits.

    Sécurité : seul le nom final de chaque fichier est conservé
    (via os.path.basename), la structure de dossiers interne au
    ZIP est ignorée — ça évite qu'un nom de fichier malveillant
    dans l'archive (ex: "../../../etc/passwd") ne sorte du dossier
    de destination prévu.
    """

    # S'assurer que le dossier de destination existe
    os.makedirs(destination_dir, exist_ok=True)

    # 1. Lire le contenu du ZIP
    content = zip_file.file.read()

    # 2. Ouvrir le ZIP depuis la mémoire
    with zipfile.ZipFile(io.BytesIO(content)) as archive:

        extracted_files = []

        # 3. Parcourir les fichiers contenus dans le ZIP
        for member in archive.infolist():

            filename = member.filename

            # 4. Ignorer les dossiers
            if member.is_dir():
                continue

            # 5. Ignorer les fichiers indésirables
            if (
                filename.startswith("__MACOSX/")
                or os.path.basename(filename) == ".DS_Store"
            ):
                continue

            # 6. Ne garder que le nom final du fichier (sécurité)
            safe_filename = os.path.basename(filename)

            # Ignorer si après nettoyage il ne reste rien (cas limite)
            if not safe_filename:
                continue

            # 7. Construire le chemin de destination
            output_path = os.path.join(destination_dir, safe_filename)

            # 8. Extraire le fichier
            with archive.open(member) as source:
                with open(output_path, "wb") as destination:
                    destination.write(source.read())

            # 9. Mémoriser le chemin extrait
            extracted_files.append(output_path)

        return extracted_files