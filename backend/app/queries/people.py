"""Person-related Cypher. No auth in this app -- 'people' double as the demo
personas a visitor can step into on the Gap Report page."""
from app.db import run_query
from app.models import Person, PersonProfile, PersonSkill, Skill

LIST_PEOPLE = """
MATCH (p:Person)
RETURN p.id AS id, p.name AS name, p.currentRoleTitle AS current_role_title
ORDER BY p.name
"""

GET_PERSON_BY_ID = """
MATCH (p:Person {id: $personId})
RETURN p.id AS id, p.name AS name, p.currentRoleTitle AS current_role_title
"""

GET_PERSON_SKILLS = """
MATCH (p:Person {id: $personId})-[hs:HAS_SKILL]->(s:Skill)
RETURN s.id AS skill_id, s.name AS skill_name, s.category AS skill_category, hs.level AS level
ORDER BY s.name
"""


def list_people() -> list[Person]:
    return [Person(**row) for row in run_query(LIST_PEOPLE)]


def get_person_profile(person_id: str) -> PersonProfile | None:
    base = run_query(GET_PERSON_BY_ID, {"personId": person_id})
    if not base:
        return None
    skill_rows = run_query(GET_PERSON_SKILLS, {"personId": person_id})
    skills = [
        PersonSkill(
            skill=Skill(id=row["skill_id"], name=row["skill_name"], category=row["skill_category"]),
            level=row["level"],
        )
        for row in skill_rows
    ]
    return PersonProfile(**base[0], skills=skills)
