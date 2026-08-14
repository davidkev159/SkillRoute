export interface Skill {
  id: string;
  name: string;
  category: string;
}

export interface SkillNode extends Skill {
  depth: number;
}

export interface Course {
  id: string;
  title: string;
  provider: string;
  duration_hours: number;
  level: string;
  url: string | null;
}

export interface Role {
  id: string;
  title: string;
  level: string;
  description: string;
}

export interface RoleSummary {
  id: string;
  title: string;
  level: string;
}

export interface RoleRequirement {
  skill: Skill;
  min_level: number;
  importance: "core" | "important" | "nice-to-have";
}

export interface RoleDetail extends Role {
  requirements: RoleRequirement[];
  people_count: number;
}

export interface SkillDetail extends Skill {
  prerequisites: SkillNode[];
  required_by_roles: RoleSummary[];
  taught_by_courses: Course[];
}

export interface Person {
  id: string;
  name: string;
  current_role_title: string | null;
}

export interface PersonSkill {
  skill: Skill;
  level: number;
}

export interface PersonProfile extends Person {
  skills: PersonSkill[];
}

export interface MissingSkill {
  skill: Skill;
  min_level: number;
  importance: "core" | "important" | "nice-to-have";
  prerequisite_chain: Skill[];
  covering_courses: Course[];
}

export interface GapAnalysisResult {
  role: RoleSummary;
  already_has: Skill[];
  missing: MissingSkill[];
  recommended_courses: Course[];
  recommended_path_hours: number;
}

export interface BottleneckSkill {
  skill: Skill;
  unlocked_role_count: number;
  unlocked_roles: RoleSummary[];
}

export interface CareerTransitionExample {
  person: Person;
  gained_skills: Skill[];
}

export interface CareerPathResult {
  from_role: RoleSummary;
  to_role: RoleSummary;
  precedent_count: number;
  commonly_gained_skills: (Skill & { person_count: number })[];
  examples: CareerTransitionExample[];
}
