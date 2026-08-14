"""
'High-leverage skills': for every skill a role requires, walk its
prerequisite chain and count, per enabling skill, how many distinct roles it
ultimately unlocks. This is a graph centrality-style question -- awkward in
SQL because it needs a recursive join per role-requirement row before the
aggregation even starts.
"""
from app.db import run_query
from app.models import BottleneckSkill, RoleSummary, Skill

GET_BOTTLENECK_SKILLS = """
MATCH (r:Role)-[:REQUIRES_SKILL]->(needed:Skill)
OPTIONAL MATCH (needed)-[:REQUIRES*1..4]->(enabler:Skill)
WITH r, needed, collect(DISTINCT enabler) + [needed] AS enablingSkills
UNWIND enablingSkills AS s
WITH s, collect(DISTINCT r) AS roles
RETURN s.id AS id, s.name AS name, s.category AS category,
       size(roles) AS unlocked_role_count,
       [x IN roles | {id: x.id, title: x.title, level: x.level}] AS unlocked_roles
ORDER BY unlocked_role_count DESC, s.name
LIMIT $limit
"""


def get_bottleneck_skills(limit: int = 10) -> list[BottleneckSkill]:
    rows = run_query(GET_BOTTLENECK_SKILLS, {"limit": limit})
    return [
        BottleneckSkill(
            skill=Skill(id=row["id"], name=row["name"], category=row["category"]),
            unlocked_role_count=row["unlocked_role_count"],
            unlocked_roles=[RoleSummary(**r) for r in row["unlocked_roles"]],
        )
        for row in rows
    ]
