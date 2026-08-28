from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config.settings import settings


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


# 5. Dépendance FastAPI : fournit une session à chaque requête,
# et la ferme automatiquement une fois la requête terminée.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()