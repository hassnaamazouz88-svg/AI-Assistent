from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config.settings import settings

#"from models import db_models" — ne doit PAS être ici,
# car Base n'est pas encore définie à ce stade du fichier.
# Ça causait une double exécution de ce fichier, avec deux Base différents.


# 1. Construire l'URL de connexion PostgreSQL
DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)


# 2. Créer le engine SQLAlchemy
engine = create_engine(DATABASE_URL)


# 3. Créer la fabrique de sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# 4. Créer Base pour les futurs modèles
class Base(DeclarativeBase):
    pass

#testing connection
if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("Connexion réussie !")

        print("Connecté à :", engine.url)

        # Import des modèles : UNIQUEMENT ici, après que Base soit définie
        from models import db_models

        print("Tables connues par SQLAlchemy :", Base.metadata.tables.keys())

        Base.metadata.create_all(bind=engine)
        print("Tables créées avec succès !")

        from sqlalchemy import inspect
        inspector = inspect(engine)
        print("Tables trouvées :", inspector.get_table_names())

    except Exception as e:
        print("Erreur :", e)