"use client";

import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

const data = [
  { name: "Hate", value: 320 },
  { name: "NSFW", value: 450 },
  { name: "Spam", value: 210 },
];

export default function AnalyticsPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Moderation Analytics</h1>

      <BarChart width={600} height={300} data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value" />
      </BarChart>
    </div>
  );
}
