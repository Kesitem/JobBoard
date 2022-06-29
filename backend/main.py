from apis.base import api_router
from core.config import settings
from db.base import Base
from db.session import engine
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from webapps.base import api_router as web_app_router


def include_router(application):
    application.include_router(api_router)
    application.include_router(web_app_router)


def configure_static(application):
    application.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    application = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(application)
    configure_static(application)
    create_tables()
    return application


app = start_application()
