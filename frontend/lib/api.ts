export type StudyRecord = {
  id: number;
  title: string;
  content: string;
  study_minutes: number;
  study_date: string;
  memo: string | null;
  created_at: string;
  updated_at: string;
};

export type StudyRecordCreate = {
  title: string;
  content: string;
  study_minutes: number;
  study_date: string;
  memo?: string | null;
};

export type GoalType = "daily" | "monthly";

export type Goal = {
  id: number;
  goal_type: GoalType;
  target_minutes: number;
  target_date: string;
  achieved_minutes: number;
  achievement_rate: number;
  is_achieved: boolean;
  created_at: string;
  updated_at: string;
};

export type GoalCreate = {
  goal_type: GoalType;
  target_minutes: number;
  target_date: string;
};

export type CalendarDay = {
  date: string;
  study_minutes: number;
  target_minutes: number | null;
  achievement_rate: number | null;
  is_achieved: boolean | null;
};

export type ProgressSummary = {
  daily: {
    date: string;
    study_minutes: number;
    target_minutes: number | null;
    achievement_rate: number | null;
    is_achieved: boolean | null;
  };
  monthly: {
    year: number;
    month: number;
    study_minutes: number;
    target_minutes: number | null;
    achievement_rate: number | null;
    is_achieved: boolean | null;
  };
  streak: {
    current_streak_days: number;
    longest_streak_days: number;
  };
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers
    }
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null);
    const message =
      typeof errorBody?.detail === "string"
        ? errorBody.detail
        : `API request failed: ${response.status}`;
    throw new Error(message);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export const api = {
  listStudyRecords: (params?: { startDate?: string; endDate?: string }) => {
    const searchParams = new URLSearchParams();
    if (params?.startDate) searchParams.set("start_date", params.startDate);
    if (params?.endDate) searchParams.set("end_date", params.endDate);
    const query = searchParams.toString();
    return request<StudyRecord[]>(`/study-records${query ? `?${query}` : ""}`);
  },
  createStudyRecord: (payload: StudyRecordCreate) =>
    request<StudyRecord>("/study-records", {
      method: "POST",
      body: JSON.stringify(payload)
    }),
  updateStudyRecord: (id: number, payload: Partial<StudyRecordCreate>) =>
    request<StudyRecord>(`/study-records/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    }),
  deleteStudyRecord: (id: number) =>
    request<void>(`/study-records/${id}`, {
      method: "DELETE"
    }),
  listGoals: (goalType?: GoalType) =>
    request<Goal[]>(`/goals${goalType ? `?goal_type=${goalType}` : ""}`),
  createGoal: (payload: GoalCreate) =>
    request<Goal>("/goals", {
      method: "POST",
      body: JSON.stringify(payload)
    }),
  updateGoal: (id: number, targetMinutes: number) =>
    request<Goal>(`/goals/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ target_minutes: targetMinutes })
    }),
  deleteGoal: (id: number) =>
    request<void>(`/goals/${id}`, {
      method: "DELETE"
    }),
  getCalendar: (year: number, month: number) =>
    request<CalendarDay[]>(`/calendar?year=${year}&month=${month}`),
  getProgress: (targetDate: string) =>
    request<ProgressSummary>(`/progress?target_date=${targetDate}`)
};

export function todayString() {
  return new Date().toISOString().slice(0, 10);
}

export function monthStartString(dateString: string) {
  return `${dateString.slice(0, 7)}-01`;
}
