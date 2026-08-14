"""
Career precedent: people who actually held role A and later role B, and what
skills they picked up that B requires but A didn't. Requires matching the
same person across two different role-history edges, ordering by date, then
diffing two skill-requirement sets per person -- a natural graph pattern,
a multi-way self-join in SQL.
"""
from app.db import run_query
from app.models import CareerPathResult, CareerTransitionExample, Person, RoleSummary, Skill

GET_ROLE_SUMMARY = """
MATCH (r:Role {id: $roleId})
RETURN r.id AS id, r.title AS title, r.level AS level
"""

# NOTE: CognoDB (v0.9.11, pre-1.0) doesn't correctly correlate inline pattern
# predicates like `WHERE (b)-[:REQUIRES_SKILL]->(gained)` to the bound `b`
# from an earlier MATCH -- it was evaluating true for skills required by ANY
# role, not just `b`. Precomputing each role's required-skill id set with a
# plain MATCH + collect (verified to work correctly) and doing the set diff
# below sidesteps that engine bug.
GET_ROLE_REQUIRED_SKILL_IDS = """
MATCH (r:Role {id: $roleId})-[:REQUIRES_SKILL]->(s:Skill)
RETURN collect(s.id) AS skillIds
"""

# Multi-hop pattern: same person, two HELD_ROLE edges ordered in time, plus
# everything they actually know -- the "commonly gained" diff against each
# role's required-skill set happens in Python (see get_career_path).
GET_PRECEDENT_PEOPLE_WITH_SKILLS = """
MATCH (p:Person)-[hr1:HELD_ROLE]->(a:Role {id: $fromRoleId})
MATCH (p)-[hr2:HELD_ROLE]->(b:Role {id: $toRoleId})
WHERE hr1.to <= hr2.from
OPTIONAL MATCH (p)-[:HAS_SKILL]->(known:Skill)
RETURN p.id AS id, p.name AS name, p.currentRoleTitle AS current_role_title,
       collect(DISTINCT {id: known.id, name: known.name, category: known.category}) AS knownSkills
"""

def get_career_path(from_role_id: str, to_role_id: str) -> CareerPathResult | None:
    from_rows = run_query(GET_ROLE_SUMMARY, {"roleId": from_role_id})
    to_rows = run_query(GET_ROLE_SUMMARY, {"roleId": to_role_id})
    if not from_rows or not to_rows:
        return None

    params = {"fromRoleId": from_role_id, "toRoleId": to_role_id}
    from_required_ids = set(run_query(GET_ROLE_REQUIRED_SKILL_IDS, {"roleId": from_role_id})[0]["skillIds"])
    to_required_ids = set(run_query(GET_ROLE_REQUIRED_SKILL_IDS, {"roleId": to_role_id})[0]["skillIds"])
    newly_required_ids = to_required_ids - from_required_ids

    precedent_rows = run_query(GET_PRECEDENT_PEOPLE_WITH_SKILLS, params)

    gained_counts: dict[str, dict] = {}
    examples: list[CareerTransitionExample] = []
    for row in precedent_rows:
        gained = [s for s in row["knownSkills"] if s.get("id") in newly_required_ids]
        for s in gained:
            entry = gained_counts.setdefault(s["id"], {**s, "person_count": 0})
            entry["person_count"] += 1
        examples.append(
            CareerTransitionExample(
                person=Person(id=row["id"], name=row["name"], current_role_title=row["current_role_title"]),
                gained_skills=[Skill(id=s["id"], name=s["name"], category=s["category"]) for s in gained],
            )
        )

    commonly_gained = sorted(gained_counts.values(), key=lambda s: (-s["person_count"], s["name"]))[:10]

    return CareerPathResult(
        from_role=RoleSummary(**from_rows[0]),
        to_role=RoleSummary(**to_rows[0]),
        precedent_count=len(precedent_rows),
        commonly_gained_skills=commonly_gained,
        examples=examples[:5],
    )
