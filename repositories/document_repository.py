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