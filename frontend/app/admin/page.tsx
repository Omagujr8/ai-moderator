import { apiFetch } from "@/lib/api";
import ContentCard from "@/components/ContentCard";

export default async function AdminPage() {
  const contents = await apiFetch("/admin/content");

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Flagged Content</h1>

      {contents.map((content: any) => (
        <ContentCard key={content.id} content={content} />
      ))}
    </div>
  );
}

