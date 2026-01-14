export async function apiFetch(
  endpoint: string,
  options: RequestInit = {}
) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}${endpoint}`,
    {
      headers: {
        "Content-Type": "application/json",
      },
      ...options,
    }
  );

  if (!res.ok) {
    throw new Error("API request failed");
  }

  return res.json();
}
