import Header from "@/components/Header";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100">
      <Header />

      <div className="p-8">
        <h2 className="text-3xl font-bold mb-6">
          学習一覧
        </h2>

        <div className="bg-white rounded-xl shadow p-6">
          <p className="text-gray-700">
            学習記録はまだありません
          </p>
        </div>
      </div>
    </main>
  );
}