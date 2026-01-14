export default function Navbar({ role }: { role: string }) {
  return (
    <nav className="flex gap-4">
      <a href="/dashboard">Dashboard</a>
      <a href="/flagged-content">Flagged</a>

      {role === "admin" && (
        <>
          <a href="/analytics">Analytics</a>
          <a href="/admin/users">Users</a>
        </>
      )}
    </nav>
  );
}
