from sqlalchemy.orm import Session
from fastapi import UploadFile

from repositories import dossier_repository
from repositories import document_repository
from storage import file_manager


async def create_dossier_with_files(
    db: Session,
    nom: str,
    files: list[UploadFile]
):
    """
    Crée un dossier et enregistre les fichiers associés.

    Toutes les opérations (création du dossier, sauvegarde des fichiers,
    création des documents) sont regroupées dans une seule transaction :
    si une erreur survient à n'importe quelle étape, tout est annulé
    (rollback en base + suppression des fichiers déjà sauvegardés sur disque).
    """
    saved_files = []

    try:
        # 1. Créer le dossier (pas encore commité, juste flush pour obtenir l'id)
        dossier = dossier_repository.create_dossier(
            db=db,
            nom=nom
        )

        # 2. Traiter chaque fichier
        for file in files:
            # Sauvegarder le fichier sur le disque
            chemin_stockage = await file_manager.save_file(
                file=file,
                dossier_id=dossier.id
            )
            saved_files.append(chemin_stockage)

            # Créer le document en base (pas encore commité)
            document_repository.create_document(
                db=db,
                nom_fichier=file.filename,
                chemin_stockage=chemin_stockage,
                dossier_id=dossier.id
            )

        # 3. Tout s'est bien passé : on valide définitivement en base
        db.commit()

        # 4. Recharger le dossier pour que la relation "documents" soit à jour
        db.refresh(dossier)

        return dossier

    except Exception:
        # Annuler toutes les opérations DB non commitées
        db.rollback()

        # Supprimer les fichiers déjà sauvegardés sur le disque
        for path in saved_files:
            file_manager.delete_file(path)

        raise