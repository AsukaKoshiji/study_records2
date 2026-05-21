"use client";

import { FormEvent, useEffect, useState } from "react";
import { api, ProgressSummary, todayString } from "@/lib/api";

export default function ProgressPage() {
  const [targetDate, setTargetDate] = useState(todayString());
  const [progress, setProgress] = useState<ProgressSummary | null>(null);
  const [error, setError] = useState("");

  const loadProgress = () => {
    setError("");
    api
      .getProgress(targetDate)
      .then(setProgress)
      .catch((err: Error) => setError(err.message));
  };

  useEffect(() => {
    loadProgress();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    loadProgress();
  };

  return (
    <>
      <header className="page-header">
        <div>
          <h1 className="page-title">進捗</h1>
          <p className="page-description">日次学習時間、月次学習時間、達成率、継続状況を確認します。</p>
        </div>
        <form className="actions" onSubmit={handleSubmit}>
          <input
            className="input"
            type="date"
            value={targetDate}
            onChange={(event) => setTargetDate(event.target.value)}
          />
          <button className="button" type="submit">
            表示
          </button>
        </form>
      </header>

      {error && <p className="message error">{error}</p>}

      <section className="grid four">
        <div className="card stat">
          <span className="stat-label">日次学習時間</span>
          <span className="stat-value">{progress?.daily.study_minutes ?? 0}分</span>
        </div>
        <div className="card stat">
          <span className="stat-label">月次学習時間</span>
          <span className="stat-value">{progress?.monthly.study_minutes ?? 0}分</span>
        </div>
        <div className="card stat">
          <span className="stat-label">現在の継続</span>
          <span className="stat-value">{progress?.streak.current_streak_days ?? 0}日</span>
        </div>
        <div className="card stat">
          <span className="stat-label">最長継続</span>
          <span className="stat-value">{progress?.streak.longest_streak_days ?? 0}日</span>
        </div>
      </section>

      <section className="grid two" style={{ marginTop: 18 }}>
        <div className="card">
          <h2 className="card-title">日次進捗</h2>
          <p>対象日: {progress?.daily.date ?? targetDate}</p>
          <p>目標時間: {progress?.daily.target_minutes ?? 0}分</p>
          <p>達成率: {progress?.daily.achievement_rate ?? 0}%</p>
          <p>
            <span className={progress?.daily.is_achieved ? "badge success" : "badge warning"}>
              {progress?.daily.is_achieved ? "達成" : "未達成"}
            </span>
          </p>
        </div>
        <div className="card">
          <h2 className="card-title">月次進捗</h2>
          <p>
            対象月: {progress?.monthly.year ?? targetDate.slice(0, 4)}年
            {progress?.monthly.month ?? Number(targetDate.slice(5, 7))}月
          </p>
          <p>目標時間: {progress?.monthly.target_minutes ?? 0}分</p>
          <p>達成率: {progress?.monthly.achievement_rate ?? 0}%</p>
          <p>
            <span className={progress?.monthly.is_achieved ? "badge success" : "badge warning"}>
              {progress?.monthly.is_achieved ? "達成" : "未達成"}
            </span>
          </p>
        </div>
      </section>
    </>
  );
}
