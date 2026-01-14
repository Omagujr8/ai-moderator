"use client";

import { apiFetch } from "@/lib/api";

export default function DecisionButtons({ id }: { id: string }) {
  async function decide(action: "approve" | "reject") {
    await apiFetch(`/admin/review/${id}`, {
      method: "POST",
      body: JSON.stringify({ action }),
    });

    alert("Decision saved");
  }

  return (
    <div className="space-x-4">
      <button
        onClick={() => decide("approve")}
        className="bg-green-600 text-white px-4 py-2 rounded"
      >
        Approve
      </button>

      <button
        onClick={() => decide("reject")}
        className="bg-red-600 text-white px-4 py-2 rounded"
      >
        Reject
      </button>
    </div>
  );
}
