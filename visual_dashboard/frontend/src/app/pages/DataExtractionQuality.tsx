import { Card } from "../components/ui/card";
import { CheckCircle, AlertTriangle } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";

export default function DataExtractionQuality() {
  const benchmarkData = [
    { id: "baseline", method: "Fall 2025 Baseline", time: 124 },
    { id: "current", method: "Current Model", time: 38 },
    { id: "target", method: "Target (Q2 2026)", time: 25 },
  ];

  const triples = [
    { subject: "Dropped Object", predicate: "type_of", object: "Safety Incident", flagged: false },
    { subject: "Pry Bar", predicate: "involved_equipment", object: "Hand Tool", flagged: false },
    { subject: "Elevated Work Area", predicate: "location_type", object: "Height Risk Zone", flagged: false },
    { subject: "Maintenance Activity", predicate: "task_context", object: "Routine Inspection", flagged: false },
    { subject: "Worker", predicate: "role", object: "Technician", flagged: true },
    { subject: "Safety Impact", predicate: "severity", object: "High", flagged: false },
  ];

  return (
    <div className="p-6 max-w-[1800px] mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900 mb-2">Data Extraction Quality</h1>
        <p className="text-gray-600">Monitor extraction accuracy and performance benchmarks</p>
      </div>

      {/* Success Meter */}
      <Card className="p-6 shadow-sm border-gray-200 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="font-semibold text-gray-900 mb-1">JSON Parse Success Rate</h2>
            <p className="text-sm text-gray-500">Across 19,820 incident reports</p>
          </div>
          <div className="flex items-center gap-3">
            <CheckCircle className="w-12 h-12 text-green-600" />
            <div>
              <p className="text-4xl font-bold text-green-600">99%</p>
              <p className="text-sm text-gray-500">Parse Rate</p>
            </div>
          </div>
        </div>
        <div className="mt-4 w-full bg-gray-200 rounded-full h-3">
          <div className="bg-green-600 h-3 rounded-full" style={{ width: "99%" }} />
        </div>
      </Card>

      {/* Split-Screen Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Raw Safety Report Text */}
        <Card className="p-6 shadow-sm border-gray-200">
          <h2 className="font-semibold text-gray-900 mb-4">Raw Safety Report Text</h2>
          <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 h-96 overflow-y-auto">
            <p className="text-sm text-gray-700 leading-relaxed font-mono">
              <strong>Incident Report #29857</strong><br />
              <strong>Date:</strong> 2026-02-24<br />
              <strong>Time:</strong> 14:35<br />
              <strong>Location:</strong> Offshore Platform A, Deck Level 3<br /><br />
              
              <strong>Narrative:</strong><br />
              During routine maintenance activities on the elevated work area at Deck Level 3, a pry bar 
              being used by the maintenance technician was inadvertently dropped from approximately 15 feet 
              above the main deck. The tool fell through the grating and landed on the deck below, narrowly 
              missing two workers who were conducting inspection activities in the area.<br /><br />
              
              The technician reported that the tool slipped from their grasp while attempting to pry open 
              a stuck access panel. The worker was wearing standard PPE including gloves, but the gloves 
              appeared to be worn and may have contributed to the loss of grip.<br /><br />
              
              No injuries were sustained, but this incident is classified as a high-severity near miss due 
              to the potential for serious injury or fatality. Immediate corrective actions included 
              implementing mandatory tool lanyards for all elevated work and replacing worn PPE.
            </p>
          </div>
        </Card>

        {/* Extracted Knowledge Triples */}
        <Card className="p-6 shadow-sm border-gray-200">
          <h2 className="font-semibold text-gray-900 mb-4">Extracted Knowledge Triples</h2>
          <div className="h-96 overflow-y-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 sticky top-0">
                <tr>
                  <th className="px-3 py-2 text-left font-medium text-gray-700 border-b">Subject</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700 border-b">Predicate</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700 border-b">Object</th>
                </tr>
              </thead>
              <tbody>
                {triples.map((triple, index) => (
                  <tr
                    key={`triple-${index}`}
                    className={`border-b ${triple.flagged ? "bg-amber-50" : ""}`}
                  >
                    <td className="px-3 py-2 text-gray-900">
                      {triple.flagged && (
                        <AlertTriangle className="w-3 h-3 inline mr-1 text-amber-600" />
                      )}
                      {triple.subject}
                    </td>
                    <td className="px-3 py-2 text-blue-600 font-mono text-xs">
                      {triple.predicate}
                    </td>
                    <td className="px-3 py-2 text-gray-700">{triple.object}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {/* Flagged Disagreements Note */}
          <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-lg">
            <div className="flex items-start gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-xs font-medium text-amber-900">Flagged Disagreement</p>
                <p className="text-xs text-amber-700 mt-1">
                  Model method variance detected on "Worker → role → Technician" triple. 
                  Confidence delta: 12% between extraction models.
                </p>
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Benchmark Results */}
      <Card className="p-6 shadow-sm border-gray-200">
        <h2 className="font-semibold text-gray-900 mb-4">Benchmark Results</h2>
        <p className="text-sm text-gray-500 mb-6">Time per 1,000 incidents (milliseconds)</p>
        
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={benchmarkData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="method" tick={{ fill: "#6b7280", fontSize: 12 }} />
            <YAxis tick={{ fill: "#6b7280", fontSize: 12 }} label={{ value: 'Time (ms)', angle: -90, position: 'insideLeft', style: { fill: '#6b7280' } }} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
            />
            <Bar dataKey="time" radius={[8, 8, 0, 0]}>
              {benchmarkData.map((entry) => (
                <Cell key={`bar-${entry.id}`} fill="#3b82f6" />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>

        <div className="mt-6 grid grid-cols-3 gap-4">
          <div className="p-4 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-900 font-medium">Baseline Performance</p>
            <p className="text-2xl font-bold text-blue-600">124ms</p>
            <p className="text-xs text-blue-700">Fall 2025</p>
          </div>
          <div className="p-4 bg-green-50 rounded-lg">
            <p className="text-sm text-green-900 font-medium">Current Performance</p>
            <p className="text-2xl font-bold text-green-600">38ms</p>
            <p className="text-xs text-green-700">69% improvement</p>
          </div>
          <div className="p-4 bg-purple-50 rounded-lg">
            <p className="text-sm text-purple-900 font-medium">Target (Q2 2026)</p>
            <p className="text-2xl font-bold text-purple-600">25ms</p>
            <p className="text-xs text-purple-700">80% total improvement</p>
          </div>
        </div>
      </Card>
    </div>
  );
}
