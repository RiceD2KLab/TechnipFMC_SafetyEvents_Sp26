import { useState, useCallback } from "react";
import { Card } from "../components/ui/card";
import { AlertTriangle } from "lucide-react";
import KgControlPanel from "../components/kg/KgControlPanel";
import KgGraphCanvas from "../components/kg/KgGraphCanvas";
import KgStatsPanel from "../components/kg/KgStatsPanel";
import KgColorLegend from "../components/kg/KgColorLegend";
import {
  useIncidents,
  useEntityTypes,
  useEntitySearch,
  useSubgraph,
} from "../hooks/useKgData";

export default function KnowledgeGraphReasoning() {
  const { incidents, loading: incidentsLoading } = useIncidents();
  const { entityTypes } = useEntityTypes();
  const { results: searchResults, loading: searchLoading, search } = useEntitySearch();
  const { data: subgraphData, loading: subgraphLoading, error: subgraphError, load: loadSubgraph } = useSubgraph();

  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [hopDepth, setHopDepth] = useState(1);
  const [entityTypeFilter, setEntityTypeFilter] = useState<string[]>(() =>
    ["INCIDENT", "EQUIPMENT", "BODY_PART", "INJURY_TYPE", "LOCATION", "ORGANIZATION", "ROOT_CAUSE_CATEGORY"]
  );

  const handleExplore = useCallback(() => {
    if (!selectedNodeId) return;
    const allTypes = entityTypes.map((et) => et.name);
    const filter =
      entityTypeFilter.length === allTypes.length || entityTypeFilter.length === 0
        ? undefined
        : entityTypeFilter;
    loadSubgraph(selectedNodeId, hopDepth, filter);
  }, [selectedNodeId, hopDepth, entityTypeFilter, entityTypes, loadSubgraph]);

  const handleSelectNode = useCallback((nodeId: string) => {
    setSelectedNodeId(nodeId);
  }, []);

  return (
    <div className="p-6 max-w-[1800px] mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900 mb-1">
          Knowledge Graph Explorer
        </h1>
        <p className="text-gray-600 text-sm">
          Browse incidents or search entities to visualize their knowledge graph
          neighborhood.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Panel - Controls */}
        <div className="lg:col-span-3">
          <KgControlPanel
            incidents={incidents}
            incidentsLoading={incidentsLoading}
            entityTypes={entityTypes}
            selectedNodeId={selectedNodeId}
            onSelectNode={handleSelectNode}
            hopDepth={hopDepth}
            onHopDepthChange={setHopDepth}
            entityTypeFilter={entityTypeFilter}
            onEntityTypeFilterChange={setEntityTypeFilter}
            onExplore={handleExplore}
            searchResults={searchResults}
            searchLoading={searchLoading}
            onSearch={search}
            exploring={subgraphLoading}
          />
        </div>

        {/* Center Panel - Graph Visualization */}
        <div className="lg:col-span-6">
          <Card className="p-5 shadow-sm border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="font-semibold text-gray-900">
                  Subgraph Visualization
                </h2>
                <p className="text-xs text-gray-500">
                  {subgraphData
                    ? `${subgraphData.stats.node_count} nodes, ${subgraphData.stats.edge_count} edges`
                    : "Select a node and click Explore"}
                </p>
              </div>
            </div>

            {subgraphData?.truncated && (
              <div className="mb-3 flex items-center gap-2 rounded-md bg-amber-50 border border-amber-200 px-3 py-2 text-xs text-amber-800">
                <AlertTriangle className="h-4 w-4 flex-shrink-0" />
                The subgraph was too large and has been capped at 500 nodes.
                Consider using entity type filters to narrow the view.
              </div>
            )}

            {subgraphError && (
              <div className="mb-3 rounded-md bg-red-50 border border-red-200 px-3 py-2 text-xs text-red-800">
                {subgraphError}
              </div>
            )}

            {subgraphLoading && (
              <div className="flex items-center justify-center h-[400px] text-gray-400">
                <div className="text-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-3" />
                  <p className="text-sm">Building subgraph...</p>
                </div>
              </div>
            )}

            {!subgraphData && !subgraphLoading && !subgraphError && (
              <div className="flex items-center justify-center h-[400px] text-gray-400">
                <div className="text-center">
                  <p className="text-sm mb-1">No subgraph loaded</p>
                  <p className="text-xs">
                    Select an incident or search for an entity, then click
                    Explore.
                  </p>
                </div>
              </div>
            )}

            {subgraphData && !subgraphLoading && (
              <>
                <KgGraphCanvas
                  nodes={subgraphData.nodes}
                  edges={subgraphData.edges}
                  entityTypes={entityTypes}
                  centerNodeId={subgraphData.center_node_id}
                />
                <div className="mt-3">
                  <KgColorLegend
                    entityTypes={entityTypes}
                    activeCounts={subgraphData.stats.entity_type_counts}
                  />
                </div>
              </>
            )}
          </Card>
        </div>

        {/* Right Panel - Stats */}
        <div className="lg:col-span-3">
          <KgStatsPanel
            stats={subgraphData?.stats ?? null}
            entityTypes={entityTypes}
            loading={subgraphLoading}
          />
        </div>
      </div>

      <p className="mt-4 text-xs text-gray-400 text-center">
        Knowledge Graph: powered by NetworkX + FastAPI
      </p>
    </div>
  );
}
