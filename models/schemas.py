from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    id: UUID
    nom_fichier: str
    statut_traitement: str

    model_config = ConfigDict(from_attributes=True)


class DossierResponse(BaseModel):
    id: UUID
    nom: str
    statut: str
    documents: list[DocumentResponse]

    model_config = ConfigDict(from_attributes=True)