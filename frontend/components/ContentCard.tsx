import FlagBadge from "./FlagBadge";
import Link from "next/link";

export default function ContentCard({ content }: any) {
  return (
    <div className="border p-4 rounded shadow-sm">
      <p className="text-sm">{content.text}</p>

      <div className="flex justify-between mt-3">
        <FlagBadge reason={content.reason} />
        <Link
          href={`/admin/review/${content.id}`}
          className="text-blue-600 underline"
        >
          Review
        </Link>
      </div>
    </div>
  );
}
