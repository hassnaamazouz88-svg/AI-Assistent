from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from config.database import get_db
from models.schemas import DossierResponse
from services import dossier_service


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