from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.config import settings
from apis.general_pages.route_homepage import general_pages_router


def include_router(application):
    application.include_router(general_pages_router)


def configure_static(application):
    application.mount("/static", StaticFiles(directory="static"), name="static")


def start_application():
    application = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(application)
    configure_static(application)
    return application


app = start_application()

