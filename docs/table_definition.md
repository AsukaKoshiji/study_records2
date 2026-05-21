
# テーブル定義書

## study_records

学習記録を日付単位で保存するテーブルです。削除は物理削除です。

| カラム名 | 型 | NULL | キー | 説明 |
|---|---|---|---|---|
| id | INT | NO | PK | 学習記録ID |
| title | VARCHAR(255) | NO |  | 学習タイトル |
| content | TEXT | NO |  | 学習内容 |
| study_minutes | INT | NO |  | 学習時間（分） |
| study_date | DATE | NO | INDEX | 学習日 |
| memo | TEXT | YES |  | メモ |
| created_at | DATETIME | NO |  | 作成日時 |
| updated_at | DATETIME | NO |  | 更新日時 |

## goals

日次・月次の学習目標を保存するテーブルです。

| カラム名 | 型 | NULL | キー | 説明 |
|---|---|---|---|---|
| id | INT | NO | PK | 目標ID |
| goal_type | ENUM('daily', 'monthly') | NO | INDEX | 目標種別 |
| target_minutes | INT | NO |  | 目標時間（分） |
| target_date | DATE | NO | INDEX | 対象日。月次目標の場合は対象月の1日 |
| created_at | DATETIME | NO |  | 作成日時 |
| updated_at | DATETIME | NO |  | 更新日時 |

Unique Key:

| 制約名 | カラム | 説明 |
|---|---|---|
| uq_goals_goal_type_target_date | goal_type, target_date | 同じ目標種別・対象日の重複登録を防止 |

## インデックス方針

| テーブル | インデックス | 目的 |
|---|---|---|
| study_records | study_date | 一覧、カレンダー、進捗集計の検索 |
| goals | goal_type | 日次・月次目標の絞り込み |
| goals | target_date | 対象日・対象月の目標検索 |
