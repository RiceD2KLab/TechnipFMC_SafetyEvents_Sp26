import { useRef, useEffect, useState, useCallback } from "react";
import type { GraphNode, GraphEdge, EntityTypeInfo } from "../../types/kg";

interface KgGraphCanvasProps {
  nodes: GraphNode[];
  edges: GraphEdge[];
  entityTypes: EntityTypeInfo[];
  centerNodeId: string;
}

const ENTITY_COLOR_MAP: Record<string, string> = {
  INCIDENT: "#E74C3C",
  EQUIPMENT: "#3498DB",
  BODY_PART: "#E67E22",
  INJURY_TYPE: "#9B59B6",
  LOCATION: "#27AE60",
  ORGANIZATION: "#1ABC9C",
  ROOT_CAUSE_CATEGORY: "#F1C40F",
};

export default function KgGraphCanvas({
  nodes,
  edges,
  entityTypes,
  centerNodeId,
}: KgGraphCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [hoveredNode, setHoveredNode] = useState<GraphNode | null>(null);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });
  const [canvasSize, setCanvasSize] = useState({ w: 800, h: 550 });

  // Build a color map from entityTypes prop, falling back to hardcoded
  const colorMap = new Map<string, string>();
  for (const et of entityTypes) {
    colorMap.set(et.name, et.color);
  }

  // Resize observer
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const ro = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width } = entry.contentRect;
        if (width > 0) {
          setCanvasSize({ w: width, h: Math.max(400, Math.min(width * 0.7, 600)) });
        }
      }
    });
    ro.observe(container);
    return () => ro.disconnect();
  }, []);

  // Scale normalized [0,1] positions to canvas pixel positions
  const toPixel = useCallback(
    (nx: number, ny: number): [number, number] => {
      const pad = 40;
      return [
        pad + nx * (canvasSize.w - 2 * pad),
        pad + ny * (canvasSize.h - 2 * pad),
      ];
    },
    [canvasSize],
  );

  // Draw
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const dpr = window.devicePixelRatio || 1;
    canvas.width = canvasSize.w * dpr;
    canvas.height = canvasSize.h * dpr;
    canvas.style.width = `${canvasSize.w}px`;
    canvas.style.height = `${canvasSize.h}px`;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, canvasSize.w, canvasSize.h);

    const nodeMap = new Map(nodes.map((n) => [n.id, n]));

    // Draw edges
    for (const edge of edges) {
      const src = nodeMap.get(edge.source);
      const tgt = nodeMap.get(edge.target);
      if (!src || !tgt) continue;

      const [x0, y0] = toPixel(src.x, src.y);
      const [x1, y1] = toPixel(tgt.x, tgt.y);

      ctx.strokeStyle = "#c0c0c0";
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(x0, y0);
      ctx.lineTo(x1, y1);
      ctx.stroke();

      // Edge label at midpoint
      const mx = (x0 + x1) / 2;
      const my = (y0 + y1) / 2;

      ctx.font = "500 9px Inter, system-ui, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";

      const label = edge.relation;
      const textWidth = ctx.measureText(label).width;

      ctx.fillStyle = "rgba(255,255,255,0.85)";
      ctx.fillRect(mx - textWidth / 2 - 3, my - 7, textWidth + 6, 14);

      ctx.fillStyle = "#6b7280";
      ctx.fillText(label, mx, my);

      if (edge.confidence != null) {
        ctx.font = "400 8px Inter, system-ui, sans-serif";
        ctx.fillStyle = "#9ca3af";
        ctx.fillText(`${Math.round(edge.confidence * 100)}%`, mx, my + 10);
      }
    }

    // Draw nodes
    for (const node of nodes) {
      const [px, py] = toPixel(node.x, node.y);
      const isCenter = node.id === centerNodeId;
      const r = isCenter ? 14 : 8;
      const color =
        colorMap.get(node.entity_type) ??
        ENTITY_COLOR_MAP[node.entity_type] ??
        "#95A5A6";

      // Circle
      ctx.beginPath();
      ctx.arc(px, py, r, 0, 2 * Math.PI);
      ctx.fillStyle = color;
      ctx.fill();
      ctx.strokeStyle = "#ffffff";
      ctx.lineWidth = 2;
      ctx.stroke();

      // Label
      const label =
        node.value.length > 30
          ? node.value.substring(0, 27) + "..."
          : node.value;
      ctx.font = isCenter
        ? "600 10px Inter, system-ui, sans-serif"
        : "400 9px Inter, system-ui, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "top";
      ctx.fillStyle = "#1f2937";
      ctx.fillText(label, px, py + r + 3);
    }
  }, [nodes, edges, canvasSize, centerNodeId, toPixel, colorMap]);

  // Hover detection
  const handleMouseMove = useCallback(
    (e: React.MouseEvent<HTMLCanvasElement>) => {
      const canvas = canvasRef.current;
      if (!canvas) return;

      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;

      let found: GraphNode | null = null;
      for (const node of nodes) {
        const [px, py] = toPixel(node.x, node.y);
        const r = node.id === centerNodeId ? 14 : 8;
        const dx = px - mx;
        const dy = py - my;
        if (dx * dx + dy * dy <= (r + 5) * (r + 5)) {
          found = node;
          break;
        }
      }

      setHoveredNode(found);
      if (found) {
        setTooltipPos({ x: e.clientX - rect.left + 12, y: e.clientY - rect.top - 10 });
      }
    },
    [nodes, toPixel, centerNodeId],
  );

  return (
    <div ref={containerRef} className="relative w-full">
      <canvas
        ref={canvasRef}
        className="w-full border border-gray-200 rounded-lg bg-white cursor-crosshair"
        onMouseMove={handleMouseMove}
        onMouseLeave={() => setHoveredNode(null)}
      />
      {hoveredNode && (
        <div
          className="absolute z-10 bg-white border border-gray-300 rounded-lg shadow-lg px-3 py-2 text-xs pointer-events-none max-w-[280px]"
          style={{ left: tooltipPos.x, top: tooltipPos.y }}
        >
          <p className="font-semibold text-gray-900 truncate">
            {hoveredNode.value}
          </p>
          <p className="text-gray-500">
            {hoveredNode.entity_type} &middot; {hoveredNode.id}
          </p>
          {Object.entries(hoveredNode.properties).length > 0 && (
            <div className="mt-1 pt-1 border-t border-gray-100 space-y-0.5">
              {Object.entries(hoveredNode.properties).map(([k, v]) => (
                <p key={k} className="text-gray-600">
                  <span className="font-medium">{k}:</span> {String(v)}
                </p>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
