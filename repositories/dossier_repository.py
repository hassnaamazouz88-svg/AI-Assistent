from sqlalchemy.orm import Session
from models.db_models import Dossier


def create_dossier(db: Session, nom: str) -> Dossier:
    """
    Crée un nouveau dossier (pas encore commité définitivement).

    Utilise flush() plutôt que commit() : ça envoie les données à
    PostgreSQL (ce qui génère l'id du dossier) sans valider la
    transaction définitivement. C'est le service appelant qui décide
    du commit final, pour permettre un rollback complet en cas d'erreur
    plus loin dans le processus (ex: échec de sauvegarde d'un fichier).
    """
    dossier = Dossier(
        nom=nom
    )
    db.add(dossier)
    db.flush()
    return dossier