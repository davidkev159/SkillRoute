from fastapi import APIRouter, HTTPException, Query

from app.models import GapAnalysisResult
from app.queries import gap_analysis as gap_q

router = APIRouter(prefix="/api/gap-analysis", tags=["gap-analysis"])


@router.get("", response_model=GapAnalysisResult)
def get_gap_analysis(
    role_id: str = Query(..., description="Target Role.id"),
    known_skill_ids: list[str] = Query(default=[], description="Skill.id values the person already has"),
):
    result = gap_q.analyze_gap(role_id=role_id, known_skill_ids=known_skill_ids)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Role '{role_id}' not found")
    return result
