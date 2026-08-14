from fastapi import APIRouter, HTTPException, Query

from app.models import CareerPathResult
from app.queries import careers as careers_q

router = APIRouter(prefix="/api/career-paths", tags=["career-paths"])


@router.get("", response_model=CareerPathResult)
def get_career_path(
    from_role_id: str = Query(..., description="Starting Role.id"),
    to_role_id: str = Query(..., description="Target Role.id"),
):
    result = careers_q.get_career_path(from_role_id, to_role_id)
    if result is None:
        raise HTTPException(status_code=404, detail="One or both roles not found")
    return result
