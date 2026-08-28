import os
import uuid
from fastapi import UploadFile

STORAGE_DIR = "storage/dossiers"


async def save_file(file: UploadFile, dossier_id: uuid.UUID) -> str:
    """
    Sauvegarde un fichier uploadé sur le disque.
    """
    dossier_path = os.path.join(STORAGE_DIR, str(dossier_id))
    os.makedirs(dossier_path, exist_ok=True)
    file_path = os.path.join(dossier_path, file.filename)

    content = await file.read()
    with open(file_path, "wb") as destination:
        destination.write(content)

    return file_path


def delete_file(path: str) -> None:
    """
    Supprime un fichier du disque s'il existe.
    """
    if os.path.exists(path):
        os.remove(path)