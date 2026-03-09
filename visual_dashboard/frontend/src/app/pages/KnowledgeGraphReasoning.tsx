import { Card } from "../components/ui/card";
import { FileDown, ChevronRight } from "lucide-react";
import { useRef, useEffect } from "react";

export default function KnowledgeGraphReasoning() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const reasoningPath = [
    { step: 1, entity: "Incident #29857", type: "Event" },
    { step: 2, entity: "Pressure Valve PV-4521", type: "Equipment", relation: "involved" },
    { step: 3, entity: "Explosion Risk", type: "Hazard", relation: "caused" },
  ];

  const graphNodes = [
    { id: "inc", label: "Incident\n#29857", x: 100, y: 200, color: "#ef4444" },
    { id: "valve", label: "Pressure Valve\nPV-4521", x: 250, y: 120, color: "#3b82f6" },
    { id: "loc", label: "Subsea\nUnit 3", x: 250, y: 280, color: "#06b6d4" },
    { id: "explosion", label: "Explosion\nRisk", x: 400, y: 120, color: "#f59e0b" },
    { id: "maintenance", label: "Deferred\nMaintenance", x: 400, y: 280, color: "#8b5cf6" },
  ];

  const edges = [
    { from: "inc", to: "valve", label: "involved", confidence: 98 },
    { from: "inc", to: "loc", label: "located_at", confidence: 100 },
    { from: "valve", to: "explosion", label: "caused", confidence: 87 },
    { from: "valve", to: "maintenance", label: "due_to", confidence: 92 },
    { from: "maintenance", to: "explosion", label: "led_to", confidence: 85 },
  ];

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw edges
    edges.forEach((edge) => {
      const fromNode = graphNodes.find((n) => n.id === edge.from);
      const toNode = graphNodes.find((n) => n.id === edge.to);
      if (!fromNode || !toNode) return;

      ctx.strokeStyle = "#9ca3af";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(fromNode.x, fromNode.y);
      ctx.lineTo(toNode.x, toNode.y);
      ctx.stroke();

      // Draw edge label
      const midX = (fromNode.x + toNode.x) / 2;
      const midY = (fromNode.y + toNode.y) / 2;

      ctx.fillStyle = "#ffffff";
      ctx.fillRect(midX - 40, midY - 12, 80, 24);

      ctx.fillStyle = "#1f2937";
      ctx.font = "400 11px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(edge.label, midX, midY);
      
      ctx.fillStyle = "#3b82f6";
      ctx.font = "600 10px sans-serif";
      ctx.fillText(`${edge.confidence}%`, midX, midY + 12);
    });

    // Draw nodes
    graphNodes.forEach((node) => {
      ctx.fillStyle = node.color;
      ctx.beginPath();
      ctx.arc(node.x, node.y, 30, 0, 2 * Math.PI);
      ctx.fill();

      ctx.strokeStyle = "#ffffff";
      ctx.lineWidth = 3;
      ctx.stroke();

      ctx.fillStyle = "#ffffff";
      ctx.font = "600 11px sans-serif";
      ctx.textAlign = "center";
      const lines = node.label.split("\n");
      lines.forEach((line, i) => {
        ctx.fillText(line, node.x, node.y - 5 + i * 12);
      });
    });
  }, []);

  return (
    <div className="p-6 max-w-[1800px] mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900 mb-2">Knowledge Graph Reasoning</h1>
        <p className="text-gray-600">Explore causal chains and evidence for incident #29857</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Panel - Reasoning Path */}
        <div className="lg:col-span-3">
          <Card className="p-6 shadow-sm border-gray-200">
            <h2 className="font-semibold text-gray-900 mb-4">Reasoning Path</h2>
            <div className="space-y-3">
              {reasoningPath.map((item, index) => (
                <div key={item.step}>
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-semibold flex-shrink-0">
                      {item.step}
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-gray-900 text-sm">{item.entity}</p>
                      <p className="text-xs text-gray-500">{item.type}</p>
                      {item.relation && (
                        <p className="text-xs text-blue-600 mt-1 flex items-center gap-1">
                          <ChevronRight className="w-3 h-3" />
                          {item.relation}
                        </p>
                      )}
                    </div>
                  </div>
                  {index < reasoningPath.length - 1 && (
                    <div className="ml-4 h-6 border-l-2 border-gray-300" />
                  )}
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Center Panel - Subgraph Visualization */}
        <div className="lg:col-span-5">
          <Card className="p-6 shadow-sm border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="font-semibold text-gray-900">Subgraph Visualization</h2>
                <p className="text-sm text-gray-500">Subject-Predicate-Object triples</p>
              </div>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 text-sm">
                <FileDown className="w-4 h-4" />
                Export to PDF
              </button>
            </div>
            <canvas
              ref={canvasRef}
              width={500}
              height={400}
              className="w-full border border-gray-200 rounded-lg bg-white"
            />
            <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-xs text-blue-900">
                <strong>Key Finding:</strong> 3-hop causal chain identified with 87% confidence. 
                Pressure valve failure directly linked to deferred maintenance schedule.
              </p>
            </div>
          </Card>
        </div>

        {/* Right Panel - Source Evidence */}
        <div className="lg:col-span-4">
          <Card className="p-6 shadow-sm border-gray-200">
            <h2 className="font-semibold text-gray-900 mb-4">Source Evidence</h2>
            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 text-sm leading-relaxed">
              <p className="text-gray-700">
                On February 24, 2026, during routine inspection at{" "}
                <span className="bg-cyan-200 px-1 rounded font-medium">Subsea Unit 3</span>, 
                technicians observed elevated pressure readings on{" "}
                <span className="bg-blue-200 px-1 rounded font-medium">Pressure Valve PV-4521</span>. 
                The valve exhibited signs of wear consistent with{" "}
                <span className="bg-purple-200 px-1 rounded font-medium">deferred maintenance</span>{" "}
                over a 6-month period. Engineers assessed the failure mode presented{" "}
                <span className="bg-amber-200 px-1 rounded font-medium">significant explosion risk</span>{" "}
                if left unaddressed. The valve was immediately isolated and scheduled for replacement.
              </p>
            </div>

            <div className="mt-4">
              <h3 className="font-medium text-gray-900 mb-2 text-sm">Extracted Entities</h3>
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-xs">
                  <div className="w-3 h-3 bg-cyan-500 rounded" />
                  <span className="text-gray-600">Location</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <div className="w-3 h-3 bg-blue-500 rounded" />
                  <span className="text-gray-600">Equipment</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <div className="w-3 h-3 bg-purple-500 rounded" />
                  <span className="text-gray-600">Root Cause</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <div className="w-3 h-3 bg-amber-500 rounded" />
                  <span className="text-gray-600">Hazard</span>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
