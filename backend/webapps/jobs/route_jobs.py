from typing import Optional

from fastapi.responses import RedirectResponse

from db.repository.jobs import list_jobs
from db.repository.jobs import retreive_job
from db.repository.jobs import create_new_job
from db.repository.jobs import search_job
from db.session import get_db
from db.models.users import User
from schemas.jobs import JobCreate
from apis.version1.route_login import get_current_user_from_token
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import responses, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.security.utils import get_authorization_scheme_param
from webapps.jobs.forms import JobCreateForm
from webapps.user import get_current_user_info

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request, db: Session = Depends(get_db)):

    user_info = get_current_user_info(request, db)
    if user_info is None:
        return RedirectResponse(url="/login/")

    jobs = list_jobs(db=db)
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "jobs": jobs, "user_info": user_info}
    )


@router.get("/jobs/detail/{id}")
def job_details(id: int, request: Request, db: Session = Depends(get_db)):
    job = retreive_job(id=id, db=db)
    return templates.TemplateResponse("jobs/details.html", {"request": request, "job": job})


@router.get("/post-a-job/")
def create_job(request: Request, db: Session = Depends(get_db)):

    user_info = get_current_user_info(request, db)
    if user_info is None:
        return RedirectResponse(url="/")

    return templates.TemplateResponse("jobs/create_job.html", {"request": request})


@router.post("/post-a-job/")
async def create_job(request: Request, db: Session = Depends(get_db)):
    form = JobCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            current_user: User = get_current_user_from_token(token=param, db=db)
            job = JobCreate(**form.__dict__)
            job = create_new_job(job=job, db=db, owner_id=current_user.id)
            return responses.RedirectResponse(
                f"/jobs/detail/{job.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            return templates.TemplateResponse("jobs/create_job.html", form.__dict__)
    return templates.TemplateResponse("jobs/create_job.html", form.__dict__)


@router.get("/delete-job/")
def show_jobs_to_delete(request: Request, db: Session = Depends(get_db)):
    jobs = list_jobs(db=db)
    return templates.TemplateResponse(
        "jobs/show_jobs_to_delete.html", {"request": request, "jobs": jobs}
    )


@router.get("/search/")
def search(
        request: Request, db: Session = Depends(get_db), query: Optional[str] = None
):
    jobs = search_job(query, db=db)
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "jobs": jobs}
    )
