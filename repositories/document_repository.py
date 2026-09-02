import uuid
from sqlalchemy.orm import Session
from models.db_models import Document


def create_document(
    db: Session,
    nom_fichier: str,
    chemin_stockage: str,
    dossier_id: uuid.UUID
) -> Document:
    """
    Crée un document et le lie à un dossier (pas encore commité définitivement).
    """
    document = Document(
        nom_fichier=nom_fichier,
        chemin_stockage=chemin_stockage,
        dossier_id=dossier_id
    )
    db.add(document)
    db.flush()
    return document


def get_by_dossier_id(db: Session, dossier_id: uuid.UUID) -> list[Document]:
    """
    Récupère tous les documents liés à un dossier.

    Utilisé par le service d'ingestion global pour savoir quels
    documents traiter.

    Args:
        db: session SQLAlchemy
        dossier_id: ID du dossier parent

    Returns:
        La liste des documents liés à ce dossier (vide si aucun).
    """
    return (
        db.query(Document)
        .filter(Document.dossier_id == dossier_id)
        .all()
    )


def update_statut(
    db: Session,
    document_id: uuid.UUID,
    statut: str
) -> Document | None:
    """
    Met à jour le statut de traitement d'un document.

    Utilisé par le service d'ingestion pour marquer un document
    comme "traite" ou "echec" après tentative d'extraction.

    Args:
        db: session SQLAlchemy
        document_id: ID du document à mettre à jour
        statut: nouveau statut ("traite", "echec", etc.)

    Returns:
        Le document mis à jour, ou None s'il n'existe pas.
    """
    document = db.query(Document).filter(Document.id == document_id).first()

    if document is None:
        return None

    document.statut_traitement = statut
    db.flush()
    return document