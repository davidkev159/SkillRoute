from fastapi import APIRouter, HTTPException, Query

from app.models import BottleneckSkill, Skill, SkillDetail
from app.queries import bottlenecks as bottlenecks_q
from app.queries import skills as skills_q

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("", response_model=list[Skill])
def list_skills():
    return skills_q.list_skills()


@router.get("/bottlenecks", response_model=list[BottleneckSkill])
def get_bottleneck_skills(limit: int = Query(default=10, ge=1, le=50)):
    return bottlenecks_q.get_bottleneck_skills(limit=limit)


@router.get("/{skill_id}", response_model=SkillDetail)
def get_skill(skill_id: str):
    skill = skills_q.get_skill_detail(skill_id)
    if skill is None:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found")
    return skill
