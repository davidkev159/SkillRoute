"""Pydantic response/request schemas shared by the routers."""
from pydantic import BaseModel


class Skill(BaseModel):
    id: str
    name: str
    category: str


class SkillNode(Skill):
    """A skill plus how deep it sits in a prerequisite chain (used when
    returning a whole prerequisite tree in one response)."""
    depth: int = 0


class Course(BaseModel):
    id: str
    title: str
    provider: str
    duration_hours: int
    level: str
    url: str | None = None


class Role(BaseModel):
    id: str
    title: str
    level: str
    description: str


class RoleSummary(BaseModel):
    id: str
    title: str
    level: str


class RoleRequirement(BaseModel):
    skill: Skill
    min_level: int
    importance: str


class RoleDetail(Role):
    requirements: list[RoleRequirement]
    people_count: int = 0


class SkillDetail(Skill):
    prerequisites: list[SkillNode]
    required_by_roles: list[RoleSummary]
    taught_by_courses: list[Course]


class Person(BaseModel):
    id: str
    name: str
    current_role_title: str | None = None


class PersonSkill(BaseModel):
    skill: Skill
    level: int


class PersonProfile(Person):
    skills: list[PersonSkill]


class MissingSkill(BaseModel):
    skill: Skill
    min_level: int
    importance: str
    prerequisite_chain: list[Skill]
    covering_courses: list[Course]


class GapAnalysisResult(BaseModel):
    role: RoleSummary
    already_has: list[Skill]
    missing: list[MissingSkill]
    recommended_courses: list[Course]
    recommended_path_hours: int


class BottleneckSkill(BaseModel):
    skill: Skill
    unlocked_role_count: int
    unlocked_roles: list[RoleSummary]


class CareerTransitionExample(BaseModel):
    person: Person
    gained_skills: list[Skill]


class CareerPathResult(BaseModel):
    from_role: RoleSummary
    to_role: RoleSummary
    precedent_count: int
    commonly_gained_skills: list[dict]
    examples: list[CareerTransitionExample]


class HealthStatus(BaseModel):
    status: str
    database: str
    detail: str | None = None
