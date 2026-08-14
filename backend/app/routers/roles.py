from fastapi import APIRouter, HTTPException

from app.models import Role, RoleDetail
from app.queries import roles as roles_q

router = APIRouter(prefix="/api/roles", tags=["roles"])


@router.get("", response_model=list[Role])
def list_roles():
    return roles_q.list_roles()


@router.get("/{role_id}", response_model=RoleDetail)
def get_role(role_id: str):
    role = roles_q.get_role_detail(role_id)
    if role is None:
        raise HTTPException(status_code=404, detail=f"Role '{role_id}' not found")
    return role
