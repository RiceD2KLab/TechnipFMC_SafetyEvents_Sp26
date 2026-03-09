import { Outlet, Link, useLocation } from "react-router";
import { Activity, BarChart3, GitBranch, Search } from "lucide-react";
import { Card } from "./ui/card";
import { useQuery } from "../context/QueryContext";

export default function Layout() {
  const location = useLocation();
  const { query, setQuery, setSearchResults } = useQuery();

  const navigation = [
    { name: "Dashboard", path: "/", icon: BarChart3 },
    { name: "Graph Reasoning", path: "/reasoning", icon: GitBranch },
    { name: "Data Extraction", path: "/extraction", icon: Search },
    { name: "Event Similarity", path: "/similarity", icon: Activity },
  ];

  const handleSearch = () => {
    if (query.trim()) {
      setSearchResults(`Searching for: "${query}"`);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="font-semibold text-gray-900">Safety Analytics Platform</h1>
                <p className="text-sm text-gray-500">TechnipFMC Industrial Safety</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="px-6">
          <div className="flex gap-1">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-2 px-4 py-3 border-b-2 transition-colors ${
                    isActive
                      ? "border-blue-600 text-blue-600"
                      : "border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="text-sm font-medium">{item.name}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Persistent Natural Language Query Section */}
      <div className="bg-white border-b border-gray-200">
        <div className="px-6 py-4 max-w-[1800px] mx-auto">
          <Card className="p-6 shadow-sm border-gray-200">
            <div className="flex items-center gap-3 mb-2">
              <Search className="w-5 h-5 text-blue-600" />
              <label className="font-medium text-gray-900">Natural Language Query</label>
            </div>
            <div className="relative">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask a safety question (e.g., What equipment is most linked to near misses?)"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder:text-gray-400"
              />
              <button 
                onClick={handleSearch}
                className="absolute right-2 top-1/2 -translate-y-1/2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
              >
                Search
              </button>
            </div>
          </Card>
        </div>
      </div>

      {/* Main Content */}
      <main>
        <Outlet />
      </main>
    </div>
  );
}
