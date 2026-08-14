"""
Idempotent seed loader for SkillRoute's CognoDB instance.

Usage (from the backend/ directory, with .env populated):
    python -m seed.seed                 # wipes the graph, then loads seed data
    python -m seed.seed --no-wipe       # loads/merges without deleting existing data
    python -m seed.seed --people 100    # generate a different number of synthetic people

Everything is loaded with MERGE keyed on each node's `id` property, so
re-running this script never creates duplicates.
"""
import argparse
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import get_settings  # noqa: E402
from app.db import close_driver, get_driver, verify_connectivity  # noqa: E402
from seed.data.catalog import (  # noqa: E402
    ROLES,
    ROLE_REQUIREMENTS,
    SKILLS,
    SKILL_PREREQUISITES,
    all_courses,
)
from seed.data.people_generator import generate_people  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("seed")

CONSTRAINTS = [
    "CREATE CONSTRAINT skill_id IF NOT EXISTS FOR (s:Skill) REQUIRE s.id IS UNIQUE",
    "CREATE CONSTRAINT role_id IF NOT EXISTS FOR (r:Role) REQUIRE r.id IS UNIQUE",
    "CREATE CONSTRAINT course_id IF NOT EXISTS FOR (c:Course) REQUIRE c.id IS UNIQUE",
    "CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE",
]

WIPE = "MATCH (n) DETACH DELETE n"

LOAD_SKILLS = """
UNWIND $rows AS row
MERGE (s:Skill {id: row.id})
SET s.name = row.name, s.category = row.category
"""

LOAD_SKILL_PREREQS = """
UNWIND $rows AS row
MATCH (s:Skill {id: row.skill}), (p:Skill {id: row.requires})
MERGE (s)-[:REQUIRES]->(p)
"""

LOAD_ROLES = """
UNWIND $rows AS row
MERGE (r:Role {id: row.id})
SET r.title = row.title, r.level = row.level, r.description = row.description
"""

LOAD_ROLE_REQUIREMENTS = """
UNWIND $rows AS row
MATCH (r:Role {id: row.role}), (s:Skill {id: row.skill})
MERGE (r)-[req:REQUIRES_SKILL]->(s)
SET req.minLevel = row.minLevel, req.importance = row.importance
"""

LOAD_COURSES = """
UNWIND $rows AS row
MERGE (c:Course {id: row.id})
SET c.title = row.title, c.provider = row.provider, c.durationHours = row.durationHours,
    c.level = row.level, c.url = row.url
"""

LOAD_COURSE_TEACHES = """
UNWIND $rows AS row
MATCH (c:Course {id: row.course}), (s:Skill {id: row.skill})
MERGE (c)-[t:TEACHES]->(s)
SET t.levelGain = row.levelGain
"""

LOAD_PEOPLE = """
UNWIND $rows AS row
MERGE (p:Person {id: row.id})
SET p.name = row.name, p.currentRoleTitle = row.current_role_title
"""

LOAD_HELD_ROLES = """
UNWIND $rows AS row
MATCH (p:Person {id: row.person}), (r:Role {id: row.role})
MERGE (p)-[hr:HELD_ROLE]->(r)
SET hr.from = row.from, hr.to = row.to
"""

LOAD_HAS_SKILLS = """
UNWIND $rows AS row
MATCH (p:Person {id: row.person}), (s:Skill {id: row.skill})
MERGE (p)-[hs:HAS_SKILL]->(s)
SET hs.level = row.level
"""

LOAD_ASPIRES_TO = """
UNWIND $rows AS row
MATCH (p:Person {id: row.person}), (r:Role {id: row.role})
MERGE (p)-[:ASPIRES_TO]->(r)
"""

COUNT_BY_LABEL = """
MATCH (n)
RETURN labels(n)[0] AS label, count(*) AS count
ORDER BY label
"""


def run(cypher: str, rows: list[dict] | None = None, database: str | None = None):
    settings = get_settings()
    get_driver().execute_query(cypher, {"rows": rows} if rows is not None else {}, database_=database or settings.neo4j_database)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-wipe", action="store_true", help="Don't delete existing data before loading")
    parser.add_argument("--people", type=int, default=60, help="Number of synthetic people to generate")
    args = parser.parse_args()

    ok, detail = verify_connectivity()
    if not ok:
        logger.error("Can't reach CognoDB: %s", detail)
        logger.error("Check NEO4J_URI / NEO4J_USERNAME / NEO4J_PASSWORD in backend/.env")
        sys.exit(1)
    logger.info("Connected to CognoDB.")

    started = time.time()

    logger.info("Ensuring uniqueness constraints...")
    for stmt in CONSTRAINTS:
        run(stmt)

    if not args.no_wipe:
        logger.info("Wiping existing graph (MATCH (n) DETACH DELETE n)...")
        run(WIPE)
    else:
        logger.info("Skipping wipe (--no-wipe): merging into existing graph.")

    logger.info("Loading %d skills...", len(SKILLS))
    run(LOAD_SKILLS, [{"id": sid, "name": name, "category": cat} for sid, name, cat in SKILLS])

    logger.info("Loading %d skill prerequisite edges...", len(SKILL_PREREQUISITES))
    run(LOAD_SKILL_PREREQS, [{"skill": s, "requires": r} for s, r in SKILL_PREREQUISITES])

    logger.info("Loading %d roles...", len(ROLES))
    run(LOAD_ROLES, [{"id": rid, "title": t, "level": lvl, "description": d} for rid, t, lvl, d in ROLES])

    logger.info("Loading %d role requirement edges...", len(ROLE_REQUIREMENTS))
    run(LOAD_ROLE_REQUIREMENTS, [
        {"role": r, "skill": s, "minLevel": lvl, "importance": imp} for r, s, lvl, imp in ROLE_REQUIREMENTS
    ])

    courses = all_courses()
    logger.info("Loading %d courses...", len(courses))
    run(LOAD_COURSES, [
        {"id": cid, "title": title, "provider": provider, "durationHours": hours, "level": level, "url": None}
        for cid, title, provider, hours, level, _teaches in courses
    ])

    teaches_rows = [
        {"course": cid, "skill": skill_id, "levelGain": gain}
        for cid, *_rest, teaches in courses
        for skill_id, gain in teaches
    ]
    logger.info("Loading %d course->skill TEACHES edges...", len(teaches_rows))
    run(LOAD_COURSE_TEACHES, teaches_rows)

    role_titles = {rid: title for rid, title, _lvl, _desc in ROLES}
    logger.info("Generating %d synthetic people...", args.people)
    people = generate_people(args.people, role_titles)

    logger.info("Loading %d people...", len(people))
    run(LOAD_PEOPLE, [
        {"id": p["id"], "name": p["name"], "current_role_title": p["current_role_title"]} for p in people
    ])

    held_role_rows = [
        {"person": p["id"], "role": hr["role_id"], "from": hr["from"], "to": hr["to"]}
        for p in people for hr in p["held_roles"]
    ]
    logger.info("Loading %d HELD_ROLE edges...", len(held_role_rows))
    run(LOAD_HELD_ROLES, held_role_rows)

    has_skill_rows = [
        {"person": p["id"], "skill": s["skill_id"], "level": s["level"]}
        for p in people for s in p["skills"]
    ]
    logger.info("Loading %d HAS_SKILL edges...", len(has_skill_rows))
    run(LOAD_HAS_SKILLS, has_skill_rows)

    aspires_rows = [{"person": p["id"], "role": p["aspires_to"]} for p in people if p["aspires_to"]]
    logger.info("Loading %d ASPIRES_TO edges...", len(aspires_rows))
    run(LOAD_ASPIRES_TO, aspires_rows)

    logger.info("Done in %.1fs. Final node counts:", time.time() - started)
    settings = get_settings()
    records, _summary, _keys = get_driver().execute_query(COUNT_BY_LABEL, database_=settings.neo4j_database)
    for record in records:
        logger.info("  %-10s %d", record["label"], record["count"])

    close_driver()


if __name__ == "__main__":
    main()
