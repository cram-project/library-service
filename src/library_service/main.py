from fastapi import FastAPI

from src.library_service.presentation.api.v1.library import api_v1_router

app = FastAPI(redirect_slashes=False)

app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"detail": "ready!"}
