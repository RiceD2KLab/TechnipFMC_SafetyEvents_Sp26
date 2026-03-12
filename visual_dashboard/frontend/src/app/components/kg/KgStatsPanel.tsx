import { Card } from "../ui/card";
import type { SubgraphStats, EntityTypeInfo } from "../../types/kg";

interface KgStatsPanelProps {
  stats: SubgraphStats | null;
  entityTypes: EntityTypeInfo[];
  loading?: boolean;
}

export default function KgStatsPanel({
  stats,
  entityTypes,
  loading,
}: KgStatsPanelProps) {
  if (loading) {
    return (
      <div className="space-y-4">
        <Card className="p-4 shadow-sm border-gray-200">
          <div className="animate-pulse space-y-3">
            <div className="h-4 bg-gray-200 rounded w-2/3" />
            <div className="h-8 bg-gray-200 rounded" />
            <div className="h-8 bg-gray-200 rounded" />
            <div className="h-8 bg-gray-200 rounded" />
          </div>
        </Card>
      </div>
    );
  }

  if (!stats) {
    return (
      <Card className="p-4 shadow-sm border-gray-200">
        <p className="text-sm text-gray-500">
          Select a node to view subgraph statistics.
        </p>
      </Card>
    );
  }

  const entityTypeMap = new Map(entityTypes.map((et) => [et.name, et]));

  return (
    <div className="space-y-4">
      <Card className="p-4 shadow-sm border-gray-200">
        <h3 className="font-semibold text-gray-900 mb-3 text-sm">
          Subgraph Statistics
        </h3>
        <div className="grid grid-cols-3 gap-3">
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900">
              {stats.node_count}
            </p>
            <p className="text-xs text-gray-500">Nodes</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900">
              {stats.edge_count}
            </p>
            <p className="text-xs text-gray-500">Edges</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900">
              {Object.keys(stats.entity_type_counts).length}
            </p>
            <p className="text-xs text-gray-500">Types</p>
          </div>
        </div>
      </Card>

      <Card className="p-4 shadow-sm border-gray-200">
        <h3 className="font-semibold text-gray-900 mb-3 text-sm">
          Entity Types
        </h3>
        <div className="space-y-2">
          {Object.entries(stats.entity_type_counts)
            .sort(([, a], [, b]) => b - a)
            .map(([type, count]) => {
              const info = entityTypeMap.get(type);
              return (
                <div
                  key={type}
                  className="flex items-center justify-between text-sm"
                >
                  <span className="flex items-center gap-2">
                    <span
                      className="inline-block h-2.5 w-2.5 rounded-full"
                      style={{
                        backgroundColor: info?.color ?? "#999",
                      }}
                    />
                    <span className="text-gray-700">
                      {info?.label ?? type}
                    </span>
                  </span>
                  <span className="font-medium text-gray-900">{count}</span>
                </div>
              );
            })}
        </div>
      </Card>

      <Card className="p-4 shadow-sm border-gray-200">
        <h3 className="font-semibold text-gray-900 mb-3 text-sm">
          Relation Types
        </h3>
        <div className="space-y-2">
          {Object.entries(stats.relation_type_counts)
            .sort(([, a], [, b]) => b - a)
            .map(([rel, count]) => (
              <div
                key={rel}
                className="flex items-center justify-between text-sm"
              >
                <span className="text-gray-700">{rel}</span>
                <span className="font-medium text-gray-900">{count}</span>
              </div>
            ))}
        </div>
      </Card>
    </div>
  );
}
