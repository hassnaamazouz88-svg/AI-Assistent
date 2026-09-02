from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
import uuid

from config.database import get_db
from models.schemas import DossierResponse
from services import dossier_service
from services import ingestion_service
from repositories import dossier_repository


router = APIRouter(
    prefix="/dossiers",
    tags=["Dossiers"]
)


@router.post("/", response_model=DossierResponse)
async def creer_dossier(
    nom: str = Form(...),
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    dossier = await dossier_service.create_dossier_with_files(
        db=db,
        nom=nom,
        files=files
    )

    return dossier


@router.post("/{dossier_id}/ingest")
def ingerer_dossier(
    dossier_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    dossier = dossier_repository.get_by_id(db, dossier_id)

    if dossier is None:
        raise HTTPException(status_code=404, detail="Dossier introuvable")

    resultat = ingestion_service.ingest_dossier(db, dossier_id)

    return resultat

