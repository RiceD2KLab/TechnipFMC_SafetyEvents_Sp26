import { Card } from "../components/ui/card";
import { Search, Filter } from "lucide-react";
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { useState } from "react";

export default function EventSimilarityDiscovery() {
  const [selectedIncident, setSelectedIncident] = useState<string | null>("29857");
  const [filters, setFilters] = useState({
    riskColor: "All",
    businessUnit: "All",
    timeRange: "10-year",
  });

  const scatterData = [
    { id: "29857", x: 5.2, y: 3.8, similarity: 100, risk: "Red", name: "Near Miss 29857" },
    { id: "28932", x: 5.4, y: 3.7, similarity: 94, risk: "Red", name: "Equipment Failure 28932" },
    { id: "27821", x: 5.1, y: 3.9, similarity: 91, risk: "Amber", name: "Pressure Incident 27821" },
    { id: "26543", x: 4.8, y: 4.2, similarity: 87, risk: "Red", name: "Dropped Object 26543" },
    { id: "25432", x: 6.2, y: 2.9, similarity: 76, risk: "Amber", name: "Valve Issue 25432" },
    { id: "24112", x: 3.8, y: 5.1, similarity: 68, risk: "Green", name: "Routine Check 24112" },
    { id: "23001", x: 4.5, y: 4.5, similarity: 72, risk: "Amber", name: "Near Miss 23001" },
    { id: "21987", x: 7.1, y: 2.2, similarity: 55, risk: "Green", name: "Inspection 21987" },
    { id: "20876", x: 2.9, y: 6.3, similarity: 48, risk: "Green", name: "Training Event 20876" },
  ];

  const topSimilar = scatterData
    .filter((d) => d.id !== selectedIncident)
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, 10);

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case "Red":
        return "#ef4444";
      case "Amber":
        return "#f59e0b";
      case "Green":
        return "#10b981";
      default:
        return "#6b7280";
    }
  };

  return (
    <div className="p-6 max-w-[1800px] mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900 mb-2">Event Similarity Discovery</h1>
        <p className="text-gray-600">Find structurally similar incidents across 10-year history</p>
      </div>

      {/* Target Incident Search */}
      <Card className="p-6 shadow-sm border-gray-200 mb-6">
        <div className="flex items-center gap-3 mb-2">
          <Search className="w-5 h-5 text-blue-600" />
          <label className="font-medium text-gray-900">Target Incident</label>
        </div>
        <div className="relative">
          <input
            type="text"
            value="Near Miss 29857"
            readOnly
            className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-white text-gray-900"
          />
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
        {/* Filters */}
        <Card className="p-6 shadow-sm border-gray-200">
          <div className="flex items-center gap-2 mb-4">
            <Filter className="w-5 h-5 text-gray-700" />
            <h2 className="font-semibold text-gray-900">Filters</h2>
          </div>

          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-gray-700 mb-2 block">Risk Color</label>
              <select
                value={filters.riskColor}
                onChange={(e) => setFilters({ ...filters, riskColor: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
              >
                <option>All</option>
                <option>Red</option>
                <option>Amber</option>
                <option>Green</option>
              </select>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-700 mb-2 block">Global Business Unit</label>
              <select
                value={filters.businessUnit}
                onChange={(e) => setFilters({ ...filters, businessUnit: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
              >
                <option>All</option>
                <option>Subsea</option>
                <option>Onshore</option>
                <option>Offshore</option>
                <option>Surface Technologies</option>
              </select>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-700 mb-2 block">Temporal Range</label>
              <select
                value={filters.timeRange}
                onChange={(e) => setFilters({ ...filters, timeRange: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
              >
                <option value="1-year">Past Year</option>
                <option value="3-year">Past 3 Years</option>
                <option value="5-year">Past 5 Years</option>
                <option value="10-year">Past 10 Years</option>
              </select>
            </div>
          </div>

          <div className="mt-6 p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-xs text-blue-900">
              <strong>Active Filters:</strong> Searching across 10-year history, all risk levels, all business units
            </p>
          </div>
        </Card>

        {/* Similarity Explorer Scatter Plot */}
        <div className="lg:col-span-3">
          <Card className="p-6 shadow-sm border-gray-200">
            <h2 className="font-semibold text-gray-900 mb-4">Similarity Explorer</h2>
            <p className="text-sm text-gray-500 mb-4">Incidents clustered by structural relevance</p>

            <ResponsiveContainer width="100%" height={400}>
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis
                  type="number"
                  dataKey="x"
                  name="Equipment Similarity"
                  tick={{ fill: "#6b7280", fontSize: 11 }}
                  label={{ value: "Equipment Similarity", position: "bottom", style: { fill: "#6b7280" } }}
                />
                <YAxis
                  type="number"
                  dataKey="y"
                  name="Root Cause Similarity"
                  tick={{ fill: "#6b7280", fontSize: 11 }}
                  label={{ value: "Root Cause Similarity", angle: -90, position: "insideLeft", style: { fill: "#6b7280" } }}
                />
                <Tooltip
                  cursor={{ strokeDasharray: "3 3" }}
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const data = payload[0].payload;
                      return (
                        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
                          <p className="font-medium text-gray-900">{data.name}</p>
                          <p className="text-sm text-gray-600">Similarity: {data.similarity}%</p>
                          <p className="text-sm text-gray-600">Risk: {data.risk}</p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Scatter data={scatterData} fill="#3b82f6">
                  {scatterData.map((entry) => (
                    <Cell
                      key={`scatter-${entry.id}`}
                      fill={entry.id === selectedIncident ? "#1e40af" : getRiskColor(entry.risk)}
                      opacity={entry.id === selectedIncident ? 1 : 0.6}
                    />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>

            <div className="mt-4 flex items-center gap-4 text-xs">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-red-500 rounded-full" />
                <span className="text-gray-600">Red Risk</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-amber-500 rounded-full" />
                <span className="text-gray-600">Amber Risk</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-green-500 rounded-full" />
                <span className="text-gray-600">Green Risk</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-blue-900 rounded-full" />
                <span className="text-gray-600">Selected Target</span>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Top 10 Similar Incidents Gallery */}
      <Card className="p-6 shadow-sm border-gray-200">
        <h2 className="font-semibold text-gray-900 mb-4">Top 10 Similar Incidents</h2>
        <p className="text-sm text-gray-500 mb-6">Ranked by structural hit rate</p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {topSimilar.map((incident, index) => (
            <div
              key={incident.id}
              className="p-4 border-2 rounded-lg hover:shadow-md transition-all cursor-pointer"
              style={{ borderColor: getRiskColor(incident.risk) }}
            >
              <div className="flex items-start justify-between mb-2">
                <div
                  className="w-8 h-8 rounded-full text-white flex items-center justify-center font-bold text-sm"
                  style={{ backgroundColor: getRiskColor(incident.risk) }}
                >
                  {index + 1}
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-gray-900">{incident.similarity}%</p>
                  <p className="text-xs text-gray-500">Hit Rate</p>
                </div>
              </div>
              <p className="font-medium text-gray-900 text-sm mb-1">{incident.name}</p>
              <p className="text-xs text-gray-600">ID: {incident.id}</p>
              
              <div className="mt-3 pt-3 border-t border-gray-200">
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <p className="text-gray-500">Equipment</p>
                    <p className="font-medium text-gray-900">{Math.round(incident.x * 10)}%</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Root Cause</p>
                    <p className="font-medium text-gray-900">{Math.round(incident.y * 10)}%</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
