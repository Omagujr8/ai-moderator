export default function FlagBadge({ reason }: { reason: string }) {
  return (
    <span className="bg-yellow-200 text-yellow-800 text-xs px-2 py-1 rounded">
      {reason}
    </span>
  );
}
