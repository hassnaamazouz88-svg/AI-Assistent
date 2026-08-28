from config.database import Base, engine
from models import db_models  # nécessaire pour enregistrer les modèles auprès de Base

print("Tables connues par SQLAlchemy :", Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)
print("Tables créées avec succès !")

from sqlalchemy import inspect
inspector = inspect(engine)
print("Tables trouvées dans PostgreSQL :", inspector.get_table_names())