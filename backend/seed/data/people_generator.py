"""
Generates synthetic Person nodes: a career history (HELD_ROLE, ordered in
time), accumulated skills (HAS_SKILL) derived from the roles they've held,
and sometimes an aspiration (ASPIRES_TO) toward a plausible next role.

Deterministic (seeded) so the graph is reproducible across seed runs.
Nobody picks up every skill their role "requires" -- that's what makes the
gap-analysis and bottleneck-skill queries return something interesting
instead of a perfectly-satisfied graph.
"""
import random

from seed.data.catalog import ROLE_REQUIREMENTS

random.seed(42)

FIRST_NAMES = [
    "Amara", "Liam", "Priya", "Noah", "Sofia", "Mateo", "Yuki", "Elena", "Kwame", "Ines",
    "Arjun", "Maya", "Theo", "Zara", "Felix", "Nadia", "Omar", "Chloe", "Diego", "Hana",
    "Leo", "Aisha", "Marcus", "Ivy", "Ravi", "Freya", "Kenji", "Lucia", "Sam", "Tara",
]
LAST_NAMES = [
    "Okafor", "Bennett", "Sharma", "Nakamura", "Rossi", "Fischer", "Dubois", "Kowalski",
    "Silva", "Haddad", "Larsen", "Novak", "Mensah", "Torres", "Petrov", "Lindqvist",
    "Abara", "Costa", "Weiss", "Nair", "Yamada", "Reyes", "Volkov", "Adeyemi", "Berg",
]

# Plausible progression edges used to build each person's career history.
PROGRESSIONS = [
    ("jr_software_engineer", "software_engineer"),
    ("software_engineer", "senior_software_engineer"),
    ("senior_software_engineer", "staff_software_engineer"),
    ("staff_software_engineer", "engineering_manager"),
    ("jr_data_analyst", "data_analyst"),
    ("data_analyst", "senior_data_analyst"),
    ("senior_data_analyst", "data_scientist"),
    ("data_analyst", "data_engineer"),
    ("data_engineer", "senior_data_engineer"),
    ("ml_engineer", "senior_ml_engineer"),
    ("data_scientist", "senior_data_scientist"),
    ("qa_engineer", "software_engineer"),
    ("frontend_engineer", "senior_software_engineer"),
    ("backend_engineer", "senior_software_engineer"),
    ("devops_engineer", "site_reliability_engineer"),
    ("data_analyst", "product_manager"),
    ("software_engineer", "ml_engineer"),
]

START_ROLES = [
    "jr_software_engineer", "jr_data_analyst", "qa_engineer", "frontend_engineer",
    "backend_engineer", "devops_engineer", "ml_engineer", "data_scientist", "product_manager",
]

NEXT_ROLES: dict[str, list[str]] = {}
for _from, _to in PROGRESSIONS:
    NEXT_ROLES.setdefault(_from, []).append(_to)

REQUIREMENTS_BY_ROLE: dict[str, list[tuple[str, int]]] = {}
for role_id, skill_id, min_level, _importance in ROLE_REQUIREMENTS:
    REQUIREMENTS_BY_ROLE.setdefault(role_id, []).append((skill_id, min_level))


def _build_career_history() -> list[str]:
    current = random.choice(START_ROLES)
    history = [current]
    steps = random.randint(0, 3)
    for _ in range(steps):
        options = NEXT_ROLES.get(current)
        if not options or random.random() > 0.7:
            break
        current = random.choice(options)
        history.append(current)
    return history


def _assign_dates(history: list[str]) -> list[tuple[str, str]]:
    """Returns [(from, to), ...] as 'YYYY-MM' strings, oldest role first,
    chronologically consistent so HELD_ROLE.to <= next HELD_ROLE.from."""
    year = 2026 - sum(2 for _ in history) - random.randint(0, 2)
    month = random.choice([1, 4, 7, 10])
    dates = []
    for _ in history:
        start = f"{year:04d}-{month:02d}"
        duration_months = random.randint(14, 30)
        month += duration_months
        year += month // 12
        month = month % 12 or 12
        end = f"{year:04d}-{month:02d}"
        dates.append((start, end))
    # Last role runs through "today" rather than an arbitrary future date.
    last_start, _ = dates[-1]
    dates[-1] = (last_start, "2026-08")
    return dates


def _accumulate_skills(history: list[str]) -> dict[str, int]:
    skills: dict[str, int] = {}
    for i, role_id in enumerate(history):
        is_current = i == len(history) - 1
        pickup_chance = 0.7 if is_current else 0.85
        for skill_id, min_level in REQUIREMENTS_BY_ROLE.get(role_id, []):
            if random.random() > pickup_chance:
                continue
            level = max(1, min(5, min_level + random.choice([-1, 0, 0, 1])))
            skills[skill_id] = max(skills.get(skill_id, 0), level)
    return skills


def generate_people(count: int, role_titles: dict[str, str]) -> list[dict]:
    used_names: set[str] = set()
    people = []
    for i in range(count):
        while True:
            name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            if name not in used_names:
                used_names.add(name)
                break

        history = _build_career_history()
        dates = _assign_dates(history)
        skills = _accumulate_skills(history)
        current_role_id = history[-1]

        aspiration = None
        if random.random() < 0.35:
            options = NEXT_ROLES.get(current_role_id)
            if options:
                aspiration = random.choice(options)

        people.append({
            "id": f"person_{i + 1:03d}",
            "name": name,
            "current_role_title": role_titles[current_role_id],
            "held_roles": [
                {"role_id": role_id, "from": frm, "to": to}
                for role_id, (frm, to) in zip(history, dates)
            ],
            "skills": [{"skill_id": sid, "level": lvl} for sid, lvl in skills.items()],
            "aspires_to": aspiration,
        })
    return people
