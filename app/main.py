from fastapi import FastAPI

from app.api.routers import main_router

from .core.config import settings

app = FastAPI(title=settings.app_title, description=settings.description)

app.include_router(main_router)
