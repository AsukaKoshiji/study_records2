"use client";

import { FormEvent, useEffect, useState } from "react";
import { api, StudyRecord, todayString } from "@/lib/api";

const emptyForm = {
  title: "",
  content: "",
  study_minutes: 60,
  study_date: todayString(),
  memo: ""
};

export default function RecordsPage() {
  const [records, setRecords] = useState<StudyRecord[]>([]);
  const [form, setForm] = useState(emptyForm);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [editingId, setEditingId] = useState<number | null>(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const loadRecords = () => {
    setError("");
    api
      .listStudyRecords({ startDate, endDate })
      .then(setRecords)
      .catch((err: Error) => setError(err.message));
  };

  useEffect(() => {
    loadRecords();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setMessage("");
    const payload = {
      ...form,
      study_minutes: Number(form.study_minutes),
      memo: form.memo || null
    };

    try {
      if (editingId) {
        await api.updateStudyRecord(editingId, payload);
        setMessage("学習記録を更新しました。");
      } else {
        await api.createStudyRecord(payload);
        setMessage("学習記録を登録しました。");
      }
      setForm({ ...emptyForm, study_date: todayString() });
      setEditingId(null);
      loadRecords();
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const startEdit = (record: StudyRecord) => {
    setEditingId(record.id);
    setForm({
      title: record.title,
      content: record.content,
      study_minutes: record.study_minutes,
      study_date: record.study_date,
      memo: record.memo ?? ""
    });
  };

  const deleteRecord = async (id: number) => {
    setError("");
    setMessage("");
    try {
      await api.deleteStudyRecord(id);
      setMessage("学習記録を削除しました。");
      loadRecords();
    } catch (err) {
      setError((err as Error).message);
    }
  };

  return (
    <>
      <header className="page-header">
        <div>
          <h1 className="page-title">学習記録</h1>
          <p className="page-description">学習タイトル、内容、時間、日付、メモを登録します。</p>
        </div>
      </header>

      <section className="grid two">
        <form className="card form-grid" onSubmit={handleSubmit}>
          <h2 className="card-title">{editingId ? "学習記録を編集" : "学習記録を追加"}</h2>
          <label className="field">
            <span className="label">学習タイトル</span>
            <input
              className="input"
              value={form.title}
              onChange={(event) => setForm({ ...form, title: event.target.value })}
              required
            />
          </label>
          <label className="field">
            <span className="label">学習内容</span>
            <textarea
              className="textarea"
              value={form.content}
              onChange={(event) => setForm({ ...form, content: event.target.value })}
              required
            />
          </label>
          <label className="field">
            <span className="label">学習時間（分）</span>
            <input
              className="input"
              type="number"
              min="1"
              value={form.study_minutes}
              onChange={(event) => setForm({ ...form, study_minutes: Number(event.target.value) })}
              required
            />
          </label>
          <label className="field">
            <span className="label">学習日</span>
            <input
              className="input"
              type="date"
              value={form.study_date}
              onChange={(event) => setForm({ ...form, study_date: event.target.value })}
              required
            />
          </label>
          <label className="field">
            <span className="label">メモ</span>
            <textarea
              className="textarea"
              value={form.memo}
              onChange={(event) => setForm({ ...form, memo: event.target.value })}
            />
          </label>
          <div className="actions">
            <button className="button" type="submit">
              {editingId ? "更新" : "登録"}
            </button>
            {editingId && (
              <button
                className="button secondary"
                type="button"
                onClick={() => {
                  setEditingId(null);
                  setForm({ ...emptyForm, study_date: todayString() });
                }}
              >
                キャンセル
              </button>
            )}
          </div>
          {message && <p className="message">{message}</p>}
          {error && <p className="message error">{error}</p>}
        </form>

        <div className="card">
          <div className="page-header">
            <div>
              <h2 className="card-title">記録一覧</h2>
            </div>
            <div className="actions">
              <input
                className="input"
                type="date"
                value={startDate}
                onChange={(event) => setStartDate(event.target.value)}
                aria-label="開始日"
              />
              <input
                className="input"
                type="date"
                value={endDate}
                onChange={(event) => setEndDate(event.target.value)}
                aria-label="終了日"
              />
              <button className="button secondary" type="button" onClick={loadRecords}>
                絞り込み
              </button>
            </div>
          </div>
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>日付</th>
                  <th>タイトル</th>
                  <th>時間</th>
                  <th>内容</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {records.map((record) => (
                  <tr key={record.id}>
                    <td>{record.study_date}</td>
                    <td>{record.title}</td>
                    <td>{record.study_minutes}分</td>
                    <td>{record.content}</td>
                    <td>
                      <div className="actions">
                        <button className="button secondary" type="button" onClick={() => startEdit(record)}>
                          編集
                        </button>
                        <button className="button danger" type="button" onClick={() => deleteRecord(record.id)}>
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
