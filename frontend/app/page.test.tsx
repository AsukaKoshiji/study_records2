import { render, screen } from "@testing-library/react";
import HomePage from "./page";

jest.mock("@/lib/api", () => ({
  api: {
    getProgress: jest.fn(() => new Promise(() => {})),
    listStudyRecords: jest.fn(() => new Promise(() => {})),
  },
  todayString: () => "2026-05-21",
}));

describe("HomePage", () => {
  it("ローディングが表示される", () => {
    render(<HomePage />);

    expect(
      screen.getByText("データを読み込み中...")
    ).toBeInTheDocument();
  });
});