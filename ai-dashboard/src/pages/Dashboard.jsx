import { Link } from "react-router-dom";

export default function Dashboard() {
  return (
    <div className="p-6">
      <h1 className="text-2xl">Dashboard</h1>

      <Link to="/upload" className="bg-blue-500 text-white p-2">
        Upload Dataset
      </Link>
    </div>
  );
}