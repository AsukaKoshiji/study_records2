import { render, screen } from "@testing-library/react";
import HomePage from "./page";
import { api } from "@/lib/api";

// 1. 本物のAPI通信を遮断し、Jestのモック関数（jest.fn）に置き換える
jest.mock("@/lib/api", () => ({
  api: {
    getProgress: jest.fn(),
    listStudyRecords: jest.fn(),
  },
  todayString: () => "2026-05-21",
}));

describe("HomePage", () => {
  // 各テストが実行される前に、モックの呼び出し履歴などを綺麗にリセットする
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("ローディングが表示される", () => {
    // 永遠に解決（resolve）しない Promise を返して、強制的にローディング状態を維持する
    (api.getProgress as jest.Mock).mockReturnValue(new Promise(() => {}));
    (api.listStudyRecords as jest.Mock).mockReturnValue(new Promise(() => {}));

    render(<HomePage />);

    // 実際のコンポーネント表記（データを読み込み中...）と一致させる
    expect(
      screen.getByText("データを読み込み中...")
    ).toBeInTheDocument();
  });

  it("APIエラー時にメッセージ表示される", async () => {
    // 意図的にAPIを失敗（Rejection）させて、コンポーネントのcatchブロックを走らせる
    (api.getProgress as jest.Mock).mockRejectedValue(new Error("API Error"));
    (api.listStudyRecords as jest.Mock).mockRejectedValue(new Error("API Error"));

    render(<HomePage />);

    // 非同期でエラーメッセージが画面に浮き出てくるのを待ってから検証（await findByText）
    expect(
      await screen.findByText("API Error")
    ).toBeInTheDocument();
  });
});

// UT-FE-003: API取得データが一覧表示される
  it("API取得データが一覧表示される", async () => {
    // 統計値は0で初期化してモック
    (api.getProgress as jest.Mock).mockResolvedValue({
      daily: { study_minutes: 0, achievement_rate: 0, is_achieved: false },
      monthly: { study_minutes: 0, achievement_rate: 0 },
      streak: { current_streak_days: 0, longest_streak_days: 0 },
    });

    // 今日の学習記録としてテストデータを1件流し込む
    (api.listStudyRecords as jest.Mock).mockResolvedValue([
      {
        id: 1,
        title: "FastAPI学習",
        study_minutes: 120,
        content: "CRUD API作成",
      },
    ]);

    render(<HomePage />);

    // 非同期でテーブル内にデータがレンダリングされるのを待って検証
    expect(
      await screen.findByText("FastAPI学習")
    ).toBeInTheDocument();

    expect(
      await screen.findByText("120分")
    ).toBeInTheDocument();

    expect(
      await screen.findByText("CRUD API作成")
    ).toBeInTheDocument();
  });