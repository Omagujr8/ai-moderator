import { apiFetch } from "@/lib/api";
import ContentCard from "@/components/ContentCard";

export default async function FlaggedContentPage() {
  const data = await apiFetch("/admin/flagged");

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Flagged Content</h1>

      {data.items.map((item: any) => (
        <ContentCard key={item.id} content={item} />
      ))}
    </div>
  );
}
