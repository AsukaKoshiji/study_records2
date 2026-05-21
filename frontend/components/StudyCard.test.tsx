import { render, screen } from "@testing-library/react";
import StudyCard from "@/components/StudyCard";

describe("StudyCard", () => {
  it("学習情報が表示される", () => {
    render(
      <StudyCard
        title="FastAPI学習"
        hours={2}
        content="CRUD API作成"
        date="2026-05-21"
      />
    );

    expect(
      screen.getByText("FastAPI学習")
    ).toBeInTheDocument();

    expect(
      screen.getByText("CRUD API作成")
    ).toBeInTheDocument();

    expect(
      screen.getByText("2時間")
    ).toBeInTheDocument();
  });
});