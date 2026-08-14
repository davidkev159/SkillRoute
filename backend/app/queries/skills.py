"""
Skill-related Cypher. `get_skill_detail` contains the project's canonical
multi-hop traversal: a variable-length `[:REQUIRES*1..5]` walk up a skill's
prerequisite DAG. In a relational schema this is a self-referencing table
that needs a recursive CTE per call; here it's one pattern.
"""
from app.db import run_query
from app.models import Course, RoleSummary, Skill, SkillDetail, SkillNode

LIST_SKILLS = """
MATCH (s:Skill)
RETURN s.id AS id, s.name AS name, s.category AS category
ORDER BY s.category, s.name
"""

# Multi-hop (2+ hops): walks the prerequisite DAG up to 5 levels deep.
GET_PREREQUISITE_CHAIN = """
MATCH (s:Skill {id: $skillId})
OPTIONAL MATCH path = (s)-[:REQUIRES*1..5]->(prereq:Skill)
WITH prereq, min(length(path)) AS depth
WHERE prereq IS NOT NULL
RETURN prereq.id AS id, prereq.name AS name, prereq.category AS category, depth
ORDER BY depth, name
"""

GET_ROLES_REQUIRING_SKILL = """
MATCH (r:Role)-[:REQUIRES_SKILL]->(s:Skill {id: $skillId})
RETURN DISTINCT r.id AS id, r.title AS title, r.level AS level
ORDER BY r.title
"""

GET_COURSES_TEACHING_SKILL = """
MATCH (c:Course)-[:TEACHES]->(s:Skill {id: $skillId})
RETURN DISTINCT c.id AS id, c.title AS title, c.provider AS provider,
       c.durationHours AS duration_hours, c.level AS level, c.url AS url
ORDER BY c.durationHours
"""

GET_SKILL_BY_ID = """
MATCH (s:Skill {id: $skillId})
RETURN s.id AS id, s.name AS name, s.category AS category
"""


def list_skills() -> list[Skill]:
    return [Skill(**row) for row in run_query(LIST_SKILLS)]


def get_skill_detail(skill_id: str) -> SkillDetail | None:
    base = run_query(GET_SKILL_BY_ID, {"skillId": skill_id})
    if not base:
        return None
    prereqs = run_query(GET_PREREQUISITE_CHAIN, {"skillId": skill_id})
    roles = run_query(GET_ROLES_REQUIRING_SKILL, {"skillId": skill_id})
    courses = run_query(GET_COURSES_TEACHING_SKILL, {"skillId": skill_id})
    return SkillDetail(
        **base[0],
        prerequisites=[SkillNode(**row) for row in prereqs],
        required_by_roles=[RoleSummary(**row) for row in roles],
        taught_by_courses=[Course(**row) for row in courses],
    )
