from fastapi import FastAPI

from api.routes.dossiers import router as dossiers_router


app = FastAPI()


app.include_router(dossiers_router)