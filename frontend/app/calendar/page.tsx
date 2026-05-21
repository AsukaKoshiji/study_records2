"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import { api, CalendarDay, todayString } from "@/lib/api";

const weekdays = ["日", "月", "火", "水", "木", "金", "土"];

export default function CalendarPage() {
  const today = todayString();
  const [year, setYear] = useState(Number(today.slice(0, 4)));
  const [month, setMonth] = useState(Number(today.slice(5, 7)));
  const [days, setDays] = useState<CalendarDay[]>([]);
  const [error, setError] = useState("");

  const loadCalendar = () => {
    setError("");
    api
      .getCalendar(year, month)
      .then(setDays)
      .catch((err: Error) => setError(err.message));
  };

  useEffect(() => {
    loadCalendar();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const cells = useMemo(() => {
    if (days.length === 0) return [];
    const firstDate = new Date(`${days[0].date}T00:00:00`);
    const blanks = Array.from({ length: firstDate.getDay() }, (_, index) => ({
      key: `blank-${index}`,
      day: null as CalendarDay | null
    }));
    return [
      ...blanks,
      ...days.map((day) => ({
        key: day.date,
        day
      }))
    ];
  }, [days]);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    loadCalendar();
  };

  return (
    <>
      <header className="page-header">
        <div>
          <h1 className="page-title">カレンダー</h1>
          <p className="page-description">日ごとの学習時間と目標達成状況を月単位で確認します。</p>
        </div>
        <form className="actions" onSubmit={handleSubmit}>
          <input
            className="input"
            type="number"
            min="1900"
            max="2100"
            value={year}
            onChange={(event) => setYear(Number(event.target.value))}
            aria-label="年"
          />
          <select
            className="select"
            value={month}
            onChange={(event) => setMonth(Number(event.target.value))}
            aria-label="月"
          >
            {Array.from({ length: 12 }, (_, index) => index + 1).map((monthNumber) => (
              <option key={monthNumber} value={monthNumber}>
                {monthNumber}月
              </option>
            ))}
          </select>
          <button className="button" type="submit">
            表示
          </button>
        </form>
      </header>

      {error && <p className="message error">{error}</p>}

      <section className="card">
        <div className="calendar-grid">
          {weekdays.map((weekday) => (
            <div className="calendar-head" key={weekday}>
              {weekday}
            </div>
          ))}
          {cells.map((cell) =>
            cell.day ? (
              <div className="calendar-day" key={cell.key}>
                <div className="calendar-date">{Number(cell.day.date.slice(8, 10))}</div>
                <div className="calendar-meta">
                  <span>{cell.day.study_minutes}分</span>
                  <span>目標: {cell.day.target_minutes ?? 0}分</span>
                  <span>
                    <span className={cell.day.is_achieved ? "badge success" : "badge warning"}>
                      {cell.day.achievement_rate ?? 0}%
                    </span>
                  </span>
                </div>
              </div>
            ) : (
              <div className="calendar-day empty" key={cell.key} />
            )
          )}
        </div>
      </section>
    </>
  );
}
