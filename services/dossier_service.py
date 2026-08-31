import os
from sqlalchemy.orm import Session
from fastapi import UploadFile

from repositories import dossier_repository
from repositories import document_repository
from storage import file_manager
from storage import zip_handler


async def create_dossier_with_files(
    db: Session,
    nom: str,
    files: list[UploadFile]
):
    """
    Crée un dossier et enregistre les fichiers associés.

    - Les fichiers normaux sont sauvegardés avec file_manager.
    - Les fichiers ZIP sont extraits avec zip_handler.
    - Chaque fichier enregistré devient un Document en base.
    - En cas d'erreur, la transaction DB est annulée et les fichiers
      déjà sauvegardés/extraits sont supprimés.
    """

    saved_files = []

    try:
        dossier = dossier_repository.create_dossier(
            db=db,
            nom=nom
        )

        destination_dir = f"storage/dossiers/{dossier.id}"

        for file in files:

            if file.filename.lower().endswith(".zip"):

                extracted_paths = zip_handler.extract_zip_contents(
                    zip_file=file,
                    destination_dir=destination_dir
                )

                saved_files.extend(extracted_paths)

                for path in extracted_paths:

                    document_repository.create_document(
                        db=db,
                        nom_fichier=os.path.basename(path),
                        chemin_stockage=path,
                        dossier_id=dossier.id
                    )

            else:

                chemin_stockage = await file_manager.save_file(
                    file=file,
                    dossier_id=dossier.id
                )

                saved_files.append(chemin_stockage)

                document_repository.create_document(
                    db=db,
                    nom_fichier=file.filename,
                    chemin_stockage=chemin_stockage,
                    dossier_id=dossier.id
                )

        db.commit()
        db.refresh(dossier)

        return dossier

    except Exception:
        db.rollback()

        for path in saved_files:
            file_manager.delete_file(path)

        raise