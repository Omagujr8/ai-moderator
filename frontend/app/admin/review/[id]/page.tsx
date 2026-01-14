import { apiFetch } from "@/lib/api";
import DecisionButtons from "@/components/DecisionButtons";

export default async function ReviewPage({ params }: any) {
  const content = await apiFetch(`/admin/content/${params.id}`);

  return (
    <div className="max-w-xl">
      <h1 className="text-xl font-bold">Review Content</h1>

      <p className="my-4 border p-3 rounded">
        {content.text}
      </p>

      <DecisionButtons id={params.id} />
    </div>
  );
}
