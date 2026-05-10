import { Link, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  Upload,
  BarChart3,
  BrainCircuit,
  LogOut,
} from "lucide-react";

export default function Sidebar() {
  const location = useLocation();

  const links = [
    {
      name: "Dashboard",
      path: "/",
      icon: <LayoutDashboard size={18} />,
    },
    {
      name: "Analytics",
      path: "/analytics",
      icon: <BarChart3 size={18} />,
    },
    {
      name: "Insights",
      path: "/insights",
      icon: <BrainCircuit size={18} />,
    },
  ];

  return (
    <div className="w-64 bg-white shadow-lg border-r">

      <div className="p-6 text-2xl font-bold border-b">
        AI Insights
      </div>

      <div className="p-4 space-y-2">

        {links.map((link) => (
          <Link
            key={link.name}
            to={link.path}
            className={`flex items-center gap-3 p-3 rounded-lg transition ${
              location.pathname === link.path
                ? "bg-blue-500 text-white"
                : "hover:bg-gray-100"
            }`}
          >
            {link.icon}
            {link.name}
          </Link>
        ))}

      </div>

      <div className="absolute bottom-0 w-64 p-4 border-t">
        <button
          onClick={() => {
            localStorage.clear();
            window.location.href = "/login";
          }}
          className="flex items-center gap-2 text-red-500"
        >
          <LogOut size={18} />
          Logout
        </button>
      </div>

    </div>
  );
}