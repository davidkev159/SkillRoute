"""
The flagship query of the app: given a role and a set of skills someone
already has, find every missing skill AND the full transitive prerequisite
chain each one needs -- in one traversal.

Why this is the "SQL would find this awkward" query the assignment asks for:
skill prerequisites are a self-referencing, variable-depth DAG. In SQL this
needs a recursive CTE, run once per missing skill (N+1), then a separate
query to find covering courses, then app-side set-cover logic to size the
course plan. Here it's one parameterised Cypher statement for the traversal.
"""
from app.db import run_query
from app.models import Course, GapAnalysisResult, MissingSkill, RoleSummary, Skill

# Multi-hop (2+ hops), the required "SQL-awkward" query: for every skill a
# role requires that the person doesn't already have, walk up to 5 levels of
# REQUIRES to collect the prerequisite chain -- also excluding anything the
# person already knows.
GET_GAP_WITH_PREREQ_CHAINS = """
MATCH (r:Role {id: $roleId})-[req:REQUIRES_SKILL]->(target:Skill)
WHERE NOT target.id IN $knownSkillIds
OPTIONAL MATCH (target)-[:REQUIRES*0..5]->(prereq:Skill)
WHERE NOT prereq.id IN $knownSkillIds
WITH target, req, collect(DISTINCT prereq) AS prereqChain
RETURN target.id AS skill_id, target.name AS skill_name, target.category AS skill_category,
       req.minLevel AS min_level, req.importance AS importance,
       [p IN prereqChain | {id: p.id, name: p.name, category: p.category}] AS prereq_chain
ORDER BY req.importance DESC, target.name
"""

GET_ALREADY_HAS = """
MATCH (r:Role {id: $roleId})-[:REQUIRES_SKILL]->(s:Skill)
WHERE s.id IN $knownSkillIds
RETURN DISTINCT s.id AS id, s.name AS name, s.category AS category
ORDER BY s.name
"""

# Courses that teach any skill in the combined "needed" set (missing skills +
# their prerequisites), used to build the recommended learning path.
GET_COVERING_COURSES = """
UNWIND $skillIds AS skillId
MATCH (c:Course)-[:TEACHES]->(s:Skill {id: skillId})
RETURN c.id AS id, c.title AS title, c.provider AS provider,
       c.durationHours AS duration_hours, c.level AS level, c.url AS url,
       collect(DISTINCT skillId) AS covers_skill_ids
"""

GET_ROLE_SUMMARY = """
MATCH (r:Role {id: $roleId})
RETURN r.id AS id, r.title AS title, r.level AS level
"""


def _greedy_course_plan(needed_skill_ids: set[str], course_rows: list[dict]) -> list[Course]:
    """Greedy set cover: repeatedly pick the course that covers the most
    still-uncovered needed skills, until everything is covered or no course
    helps anymore. Keeps the recommended path short rather than dumping
    every matching course on the user."""
    remaining = set(needed_skill_ids)
    candidates = [dict(row) for row in course_rows]
    plan: list[Course] = []
    while remaining:
        best = max(candidates, key=lambda c: len(set(c["covers_skill_ids"]) & remaining), default=None)
        if best is None or not (set(best["covers_skill_ids"]) & remaining):
            break
        plan.append(Course(**{k: v for k, v in best.items() if k != "covers_skill_ids"}))
        remaining -= set(best["covers_skill_ids"])
        candidates.remove(best)
    return plan


def analyze_gap(role_id: str, known_skill_ids: list[str]) -> GapAnalysisResult | None:
    role_rows = run_query(GET_ROLE_SUMMARY, {"roleId": role_id})
    if not role_rows:
        return None

    gap_rows = run_query(GET_GAP_WITH_PREREQ_CHAINS, {"roleId": role_id, "knownSkillIds": known_skill_ids})
    already_has_rows = run_query(GET_ALREADY_HAS, {"roleId": role_id, "knownSkillIds": known_skill_ids})

    needed_skill_ids: set[str] = set()
    missing: list[MissingSkill] = []
    for row in gap_rows:
        chain = [Skill(**p) for p in row["prereq_chain"]]
        needed_skill_ids.add(row["skill_id"])
        needed_skill_ids.update(s.id for s in chain)
        missing.append(
            MissingSkill(
                skill=Skill(id=row["skill_id"], name=row["skill_name"], category=row["skill_category"]),
                min_level=row["min_level"],
                importance=row["importance"],
                prerequisite_chain=chain,
                covering_courses=[],  # filled in below once we know the plan
            )
        )

    course_rows = run_query(GET_COVERING_COURSES, {"skillIds": list(needed_skill_ids)}) if needed_skill_ids else []
    plan = _greedy_course_plan(needed_skill_ids, course_rows)

    # Attach the courses relevant to each missing skill for display.
    course_by_id = {c.id: c for c in plan}
    covers_by_skill: dict[str, list[Course]] = {}
    for row in course_rows:
        if row["id"] not in course_by_id:
            continue
        for skill_id in row["covers_skill_ids"]:
            covers_by_skill.setdefault(skill_id, []).append(course_by_id[row["id"]])
    for m in missing:
        m.covering_courses = covers_by_skill.get(m.skill.id, [])

    return GapAnalysisResult(
        role=RoleSummary(**role_rows[0]),
        already_has=[Skill(**row) for row in already_has_rows],
        missing=missing,
        recommended_courses=plan,
        recommended_path_hours=sum(c.duration_hours for c in plan),
    )
