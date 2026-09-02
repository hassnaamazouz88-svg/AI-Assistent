import uuid

from sqlalchemy.orm import Session

from repositories import dossier_repository
from repositories import document_repository

from core.ingestion.pipeline import process_document


def ingest_dossier(db: Session, dossier_id: uuid.UUID) -> dict:
    """
    Traite tous les documents d'un dossier.

    Pour chaque document :
        1. Récupère son chemin de stockage
        2. Lance process_document()
        3. Si le traitement réussit :
           - met le document à "traite"
        4. Si le traitement échoue :
           - met le document à "echec"
           - enregistre l'erreur

    Un document en échec n'empêche pas le traitement
    des autres documents.

    À terme, cette fonction pourra également lancer :
        extraction → chunking → embeddings → ChromaDB

    Args:
        db: session SQLAlchemy
        dossier_id: UUID du dossier à traiter

    Returns:
        dict:
        {
            "traites": [...],
            "echecs": [...]
        }
    """

    # ---------------------------------------------------------
    # 1. Récupérer tous les documents du dossier
    # ---------------------------------------------------------

    documents = document_repository.get_by_dossier_id(
        db,
        dossier_id
    )

    traites = []
    echecs = []

    # ---------------------------------------------------------
    # 2. Traiter chaque document indépendamment
    # ---------------------------------------------------------

    for document in documents:

        try:
            # Extraction du texte.
            #
            # process_document() se charge lui-même de :
            # PDF / DOCX / DOC / XLSX
            # + OCR si nécessaire.
            texte = process_document(
                document.chemin_stockage
            )

            # -------------------------------------------------
            # TODO :
            # chunking + embeddings + ChromaDB
            # -------------------------------------------------
            #
            # Exemple futur :
            #
            # chunks = chunk_text(texte)
            # embeddings = create_embeddings(chunks)
            # vector_store.add(...)
            #
            # -------------------------------------------------

            # Document correctement traité
            document_repository.update_statut(
                db,
                document.id,
                "traite"
            )

            traites.append(
                document.nom_fichier
            )

        except Exception as e:

            # Une erreur sur ce document ne doit pas
            # interrompre le traitement des autres.
            document_repository.update_statut(
                db,
                document.id,
                "echec"
            )

            echecs.append({
                "fichier": document.nom_fichier,
                "erreur": str(e)
            })

    # ---------------------------------------------------------
    # 3. Sauvegarder les statuts des documents
    # ---------------------------------------------------------

    db.commit()

    # ---------------------------------------------------------
    # 4. Mettre le dossier à "pret"
    # ---------------------------------------------------------

    dossier_repository.update_statut(
        db,
        dossier_id,
        "pret"
    )

    db.commit()

    # ---------------------------------------------------------
    # 5. Retourner le résumé
    # ---------------------------------------------------------

    return {
        "traites": traites,
        "echecs": echecs
    }