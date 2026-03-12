import { TrendingUp, Network, CheckCircle, Share2 } from "lucide-react";
import { Card } from "../components/ui/card";
import GraphTopology from "../components/GraphTopology";
import RecentActivity from "../components/RecentActivity";

export default function MainDashboard() {
  const metrics = [
    { label: "Total Incidents", value: "19,820", icon: TrendingUp, color: "text-blue-600" },
    { label: "Graph Density (Mean Degree)", value: "2.5", icon: Network, color: "text-indigo-600" },
    { label: "Schema Compliance", value: "100%", icon: CheckCircle, color: "text-green-600" },
    { label: "Giant Component Ratio", value: "0.85", icon: Share2, color: "text-purple-600" },
  ];

  return (
    <div className="p-6 max-w-[1800px] mx-auto">
      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <Card key={metric.label} className="p-6 shadow-sm border-gray-200">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">{metric.label}</p>
                  <p className="text-3xl font-semibold text-gray-900">{metric.value}</p>
                </div>
                <div className={`p-3 bg-gray-50 rounded-lg ${metric.color}`}>
                  <Icon className="w-6 h-6" />
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Graph Topology - Takes 2 columns */}
        <div className="lg:col-span-2">
          <GraphTopology />
        </div>

        {/* Recent Activity - Takes 1 column */}
        <div>
          <RecentActivity />
        </div>
      </div>
    </div>
  );
}
