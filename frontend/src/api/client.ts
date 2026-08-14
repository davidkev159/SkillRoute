import type {
  BottleneckSkill,
  CareerPathResult,
  GapAnalysisResult,
  PersonProfile,
  Person,
  Role,
  RoleDetail,
  Skill,
  SkillDetail,
} from "./types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${BASE_URL}${path}`);
  } catch {
    // Network failure -- backend process down, DNS issue, CORS, etc.
    throw new ApiError("Can't reach the SkillRoute API. Is the backend running?", 0);
  }
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail ?? detail;
    } catch {
      // response wasn't JSON -- fall back to statusText
    }
    throw new ApiError(detail, res.status);
  }
  return res.json();
}

export const api = {
  health: () => request<{ status: string; database: string; detail: string | null }>("/api/health"),

  listRoles: () => request<Role[]>("/api/roles"),
  getRole: (id: string) => request<RoleDetail>(`/api/roles/${encodeURIComponent(id)}`),

  listSkills: () => request<Skill[]>("/api/skills"),
  getSkill: (id: string) => request<SkillDetail>(`/api/skills/${encodeURIComponent(id)}`),
  getBottlenecks: (limit = 10) => request<BottleneckSkill[]>(`/api/skills/bottlenecks?limit=${limit}`),

  listPeople: () => request<Person[]>("/api/people"),
  getPerson: (id: string) => request<PersonProfile>(`/api/people/${encodeURIComponent(id)}`),

  getGapAnalysis: (roleId: string, knownSkillIds: string[]) => {
    const params = new URLSearchParams({ role_id: roleId });
    knownSkillIds.forEach((id) => params.append("known_skill_ids", id));
    return request<GapAnalysisResult>(`/api/gap-analysis?${params.toString()}`);
  },

  getCareerPath: (fromRoleId: string, toRoleId: string) => {
    const params = new URLSearchParams({ from_role_id: fromRoleId, to_role_id: toRoleId });
    return request<CareerPathResult>(`/api/career-paths?${params.toString()}`);
  },
};
