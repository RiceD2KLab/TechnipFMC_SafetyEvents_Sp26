import type { EntityTypeInfo } from "../../types/kg";

interface KgColorLegendProps {
  entityTypes: EntityTypeInfo[];
  activeCounts: Record<string, number>;
}

export default function KgColorLegend({
  entityTypes,
  activeCounts,
}: KgColorLegendProps) {
  const active = entityTypes.filter((et) => (activeCounts[et.name] ?? 0) > 0);

  if (active.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-4 text-xs text-gray-600">
      {active.map((et) => (
        <span key={et.name} className="flex items-center gap-1.5">
          <span
            className="inline-block h-3 w-3 rounded-full"
            style={{ backgroundColor: et.color }}
          />
          {et.label}
        </span>
      ))}
    </div>
  );
}
