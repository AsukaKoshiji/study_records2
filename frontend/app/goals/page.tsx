"use client";

import { FormEvent, useEffect, useState } from "react";
import { api, Goal, GoalType, monthStartString, todayString } from "@/lib/api";

export default function GoalsPage() {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [goalType, setGoalType] = useState<GoalType>("daily");
  const [targetMinutes, setTargetMinutes] = useState(120);
  const [targetDate, setTargetDate] = useState(todayString());
  const [filterType, setFilterType] = useState<GoalType | "">("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const loadGoals = () => {
    setError("");
    api
      .listGoals(filterType || undefined)
      .then(setGoals)
      .catch((err: Error) => setError(err.message));
  };

  useEffect(() => {
    loadGoals();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleGoalTypeChange = (value: GoalType) => {
    setGoalType(value);
    if (value === "monthly") {
      setTargetDate(monthStartString(targetDate));
    }
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setMessage("");
    setError("");

    try {
      await api.createGoal({
        goal_type: goalType,
        target_minutes: Number(targetMinutes),
        target_date: goalType === "monthly" ? monthStartString(targetDate) : targetDate
      });
      setMessage("目標を登録しました。");
      loadGoals();
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const updateGoal = async (goal: Goal) => {
    const nextMinutes = Number(window.prompt("新しい目標時間（分）", String(goal.target_minutes)));
    if (!Number.isFinite(nextMinutes) || nextMinutes <= 0) return;
    setMessage("");
    setError("");
    try {
      await api.updateGoal(goal.id, nextMinutes);
      setMessage("目標を更新しました。");
      loadGoals();
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const deleteGoal = async (id: number) => {
    setMessage("");
    setError("");
    try {
      await api.deleteGoal(id);
      setMessage("目標を削除しました。");
      loadGoals();
    } catch (err) {
      setError((err as Error).message);
    }
  };

  return (
    <>
      <header className="page-header">
        <div>
          <h1 className="page-title">目標登録</h1>
          <p className="page-description">日次または月次の学習目標時間を設定します。</p>
        </div>
      </header>

      <section className="grid two">
        <form className="card form-grid" onSubmit={handleSubmit}>
          <h2 className="card-title">目標を追加</h2>
          <label className="field">
            <span className="label">目標単位</span>
            <select
              className="select"
              value={goalType}
              onChange={(event) => handleGoalTypeChange(event.target.value as GoalType)}
            >
              <option value="daily">日次</option>
              <option value="monthly">月次</option>
            </select>
          </label>
          <label className="field">
            <span className="label">目標時間（分）</span>
            <input
              className="input"
              type="number"
              min="1"
              value={targetMinutes}
              onChange={(event) => setTargetMinutes(Number(event.target.value))}
              required
            />
          </label>
          <label className="field">
            <span className="label">{goalType === "daily" ? "対象日" : "対象月"}</span>
            <input
              className="input"
              type="date"
              value={targetDate}
              onChange={(event) => setTargetDate(event.target.value)}
              required
            />
          </label>
          <button className="button" type="submit">
            登録
          </button>
          {message && <p className="message">{message}</p>}
          {error && <p className="message error">{error}</p>}
        </form>

        <div className="card">
          <div className="page-header">
            <div>
              <h2 className="card-title">目標一覧</h2>
            </div>
            <div className="actions">
              <select
                className="select"
                value={filterType}
                onChange={(event) => setFilterType(event.target.value as GoalType | "")}
                aria-label="目標種別で絞り込み"
              >
                <option value="">すべて</option>
                <option value="daily">日次</option>
                <option value="monthly">月次</option>
              </select>
              <button className="button secondary" type="button" onClick={loadGoals}>
                絞り込み
              </button>
            </div>
          </div>
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>単位</th>
                  <th>対象日</th>
                  <th>目標</th>
                  <th>実績</th>
                  <th>達成率</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {goals.map((goal) => (
                  <tr key={goal.id}>
                    <td>{goal.goal_type === "daily" ? "日次" : "月次"}</td>
                    <td>{goal.target_date}</td>
                    <td>{goal.target_minutes}分</td>
                    <td>{goal.achieved_minutes}分</td>
                    <td>
                      <span className={goal.is_achieved ? "badge success" : "badge warning"}>
                        {goal.achievement_rate}%
                      </span>
                    </td>
                    <td>
                      <div className="actions">
                        <button className="button secondary" type="button" onClick={() => updateGoal(goal)}>
                          編集
                        </button>
                        <button className="button danger" type="button" onClick={() => deleteGoal(goal.id)}>
                          削除
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </>
  );
}
