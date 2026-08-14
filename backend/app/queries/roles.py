"""Role-related Cypher."""
from app.db import run_query
from app.models import Role, RoleDetail, RoleRequirement, Skill

LIST_ROLES = """
MATCH (r:Role)
RETURN r.id AS id, r.title AS title, r.level AS level, r.description AS description
ORDER BY r.title
"""

GET_ROLE_BY_ID = """
MATCH (r:Role {id: $roleId})
RETURN r.id AS id, r.title AS title, r.level AS level, r.description AS description
"""

GET_ROLE_REQUIREMENTS = """
MATCH (r:Role {id: $roleId})-[req:REQUIRES_SKILL]->(s:Skill)
RETURN s.id AS skill_id, s.name AS skill_name, s.category AS skill_category,
       req.minLevel AS min_level, req.importance AS importance
ORDER BY req.importance DESC, s.name
"""

COUNT_PEOPLE_IN_ROLE = """
MATCH (:Person)-[:HELD_ROLE]->(r:Role {id: $roleId})
RETURN count(*) AS peopleCount
"""


def list_roles() -> list[Role]:
    return [Role(**row) for row in run_query(LIST_ROLES)]


def get_role_detail(role_id: str) -> RoleDetail | None:
    base = run_query(GET_ROLE_BY_ID, {"roleId": role_id})
    if not base:
        return None
    reqs = run_query(GET_ROLE_REQUIREMENTS, {"roleId": role_id})
    people_count = run_query(COUNT_PEOPLE_IN_ROLE, {"roleId": role_id})[0]["peopleCount"]
    requirements = [
        RoleRequirement(
            skill=Skill(id=row["skill_id"], name=row["skill_name"], category=row["skill_category"]),
            min_level=row["min_level"],
            importance=row["importance"],
        )
        for row in reqs
    ]
    return RoleDetail(**base[0], requirements=requirements, people_count=people_count)
