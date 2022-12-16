from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from apis.version1.route_login import get_current_user_from_token
from db.models.users import User
from fastapi import HTTPException


def get_current_user_info(request: Request, db: Session):
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(
        token
    )  # scheme will hold "Bearer" and param will hold actual token value
    try:
        current_user: User = get_current_user_from_token(token=param, db=db)
    except HTTPException as e:
        current_user = None
    user_info = {}
    if current_user is not None:
        user_info["name"] = current_user.username
    else:
        user_info = None
    return user_info
