import { apiFetch } from "@/lib/api";

export default async function AnalyticsPage() {
  const stats = await apiFetch("/analytics/overview");

  return (
    <div>
      <h1 className="text-2xl font-bold">Analytics</h1>
      <pre className="bg-gray-100 p-4 rounded mt-4">
        {JSON.stringify(stats, null, 2)}
      </pre>
    </div>
  );
}
