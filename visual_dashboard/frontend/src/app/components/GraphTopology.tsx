import { Card } from "./ui/card";
import { useEffect, useRef, useState } from "react";

interface Node {
  id: string;
  type: string;
  count: number;
  x: number;
  y: number;
  color: string;
}

export default function GraphTopology() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [hoveredNode, setHoveredNode] = useState<Node | null>(null);

  const entityTypes = [
    { type: "Equipment", count: 5420, color: "#3b82f6" },
    { type: "Injury Type", count: 1230, color: "#8b5cf6" },
    { type: "Location", count: 3890, color: "#06b6d4" },
    { type: "Personnel", count: 2150, color: "#f59e0b" },
    { type: "Root Cause", count: 890, color: "#ef4444" },
  ];

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // Generate node positions in a circular layout
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) / 3;

    const nodes: Node[] = entityTypes.map((entity, index) => {
      const angle = (index / entityTypes.length) * 2 * Math.PI - Math.PI / 2;
      return {
        id: entity.type,
        type: entity.type,
        count: entity.count,
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
        color: entity.color,
      };
    });

    // Draw connections between nodes
    ctx.strokeStyle = "#e5e7eb";
    ctx.lineWidth = 1;
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        ctx.beginPath();
        ctx.moveTo(nodes[i].x, nodes[i].y);
        ctx.lineTo(nodes[j].x, nodes[j].y);
        ctx.stroke();
      }
    }

    // Draw nodes
    nodes.forEach((node) => {
      const nodeRadius = Math.sqrt(node.count) / 3;

      // Node circle
      ctx.fillStyle = node.color;
      ctx.beginPath();
      ctx.arc(node.x, node.y, nodeRadius, 0, 2 * Math.PI);
      ctx.fill();

      // White border
      ctx.strokeStyle = "#ffffff";
      ctx.lineWidth = 3;
      ctx.stroke();

      // Node label
      ctx.fillStyle = "#1f2937";
      ctx.font = "600 12px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(node.type, node.x, node.y - nodeRadius - 10);

      // Count label
      ctx.fillStyle = "#6b7280";
      ctx.font = "400 11px sans-serif";
      ctx.fillText(node.count.toLocaleString(), node.x, node.y - nodeRadius - 24);
    });
  }, []);

  return (
    <Card className="p-6 shadow-sm border-gray-200">
      <div className="mb-4">
        <h2 className="font-semibold text-gray-900">Graph Topology</h2>
        <p className="text-sm text-gray-500">Entity type breakdowns and relationships</p>
      </div>

      <div className="relative">
        <canvas
          ref={canvasRef}
          width={800}
          height={400}
          className="w-full border border-gray-200 rounded-lg bg-white"
        />
      </div>

      {/* Legend */}
      <div className="mt-4 flex flex-wrap gap-4">
        {entityTypes.map((entity) => (
          <div key={entity.type} className="flex items-center gap-2">
            <div
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: entity.color }}
            />
            <span className="text-xs text-gray-600">
              {entity.type} ({entity.count.toLocaleString()})
            </span>
          </div>
        ))}
      </div>
    </Card>
  );
}
