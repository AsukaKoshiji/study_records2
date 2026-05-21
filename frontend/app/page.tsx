"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api, ProgressSummary, StudyRecord, todayString } from "@/lib/api";

export default function HomePage() {
  const [progress, setProgress] = useState<ProgressSummary | null>(null);
  const [records, setRecords] = useState<StudyRecord[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const today = todayString();
    Promise.all([
      api.getProgress(today),
      api.listStudyRecords({ startDate: today, endDate: today })
    ])
      .then(([progressResult, recordResult]) => {
        setProgress(progressResult);
        setRecords(recordResult);
      })
      .catch((err: Error) => setError(err.message));
  }, []);

  return (
    <>
      <header className="page-header">
        <div>
          <h1 className="page-title">学習ダッシュボード</h1>
          <p className="page-description">今日の学習時間、月次進捗、継続状況を確認します。</p>
        </div>
        <Link className="button" href="/records">
          学習記録を追加
        </Link>
      </header>

      {error && <p className="message error">{error}</p>}

      <section className="grid four">
        <div className="card stat">
          <span className="stat-label">今日の学習</span>
          <span className="stat-value">{progress?.daily.study_minutes ?? 0}分</span>
        </div>
        <div className="card stat">
          <span className="stat-label">今日の達成率</span>
          <span className="stat-value">
            {progress?.daily.achievement_rate ?? 0}%
          </span>
        </div>
        <div className="card stat">
          <span className="stat-label">月次学習</span>
          <span className="stat-value">{progress?.monthly.study_minutes ?? 0}分</span>
        </div>
        <div className="card stat">
          <span className="stat-label">現在の継続</span>
          <span className="stat-value">{progress?.streak.current_streak_days ?? 0}日</span>
        </div>
      </section>

      <section className="grid two" style={{ marginTop: 18 }}>
        <div className="card">
          <h2 className="card-title">今日の状態</h2>
          <div className="grid">
            <p>
              <span className={progress?.daily.is_achieved ? "badge success" : "badge warning"}>
                {progress?.daily.is_achieved ? "日次目標達成" : "日次目標未達成"}
              </span>
            </p>
            <p>
              月次達成率: <strong>{progress?.monthly.achievement_rate ?? 0}%</strong>
            </p>
            <p>
              最長継続日数: <strong>{progress?.streak.longest_streak_days ?? 0}日</strong>
            </p>
          </div>
        </div>
        <div className="card">
          <h2 className="card-title">今日の学習記録</h2>
          {records.length === 0 ? (
            <p className="page-description">今日の記録はまだありません。</p>
          ) : (
            <div className="table-wrap">
              <table className="table">
                <thead>
                  <tr>
                    <th>タイトル</th>
                    <th>時間</th>
                    <th>内容</th>
                  </tr>
                </thead>
                <tbody>
                  {records.map((record) => (
                    <tr key={record.id}>
                      <td>{record.title}</td>
                      <td>{record.study_minutes}分</td>
                      <td>{record.content}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </section>
    </>
  );
}
