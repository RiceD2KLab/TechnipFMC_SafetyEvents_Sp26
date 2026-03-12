import { useState } from "react";
import { Card } from "../ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "../ui/tabs";
import { Checkbox } from "../ui/checkbox";
import { Search, Loader2 } from "lucide-react";
import KgCombobox from "./KgCombobox";
import type {
  IncidentOption,
  EntityTypeInfo,
  EntitySearchResult,
} from "../../types/kg";

interface KgControlPanelProps {
  incidents: IncidentOption[];
  incidentsLoading: boolean;
  entityTypes: EntityTypeInfo[];
  selectedNodeId: string | null;
  onSelectNode: (nodeId: string) => void;
  hopDepth: number;
  onHopDepthChange: (hops: number) => void;
  entityTypeFilter: string[];
  onEntityTypeFilterChange: (types: string[]) => void;
  onExplore: () => void;
  // Entity search
  searchResults: EntitySearchResult[];
  searchLoading: boolean;
  onSearch: (entityType: string | undefined, valuePattern: string) => void;
  exploring: boolean;
}

export default function KgControlPanel({
  incidents,
  incidentsLoading,
  entityTypes,
  selectedNodeId,
  onSelectNode,
  hopDepth,
  onHopDepthChange,
  entityTypeFilter,
  onEntityTypeFilterChange,
  onExplore,
  searchResults,
  searchLoading,
  onSearch,
  exploring,
}: KgControlPanelProps) {
  const [searchType, setSearchType] = useState<string>("ALL");
  const [searchPattern, setSearchPattern] = useState("");

  const handleSearchSubmit = () => {
    onSearch(searchType === "ALL" ? undefined : searchType, searchPattern);
  };

  const handleToggleEntityType = (name: string) => {
    if (entityTypeFilter.includes(name)) {
      onEntityTypeFilterChange(entityTypeFilter.filter((t) => t !== name));
    } else {
      onEntityTypeFilterChange([...entityTypeFilter, name]);
    }
  };

  const allSelected = entityTypeFilter.length === entityTypes.length;

  return (
    <Card className="p-4 shadow-sm border-gray-200 space-y-5">
      <h2 className="font-semibold text-gray-900 text-sm">KG Explorer</h2>

      {/* Search Mode Tabs */}
      <Tabs defaultValue="browse">
        <TabsList className="w-full">
          <TabsTrigger value="browse" className="text-xs">
            Browse Incidents
          </TabsTrigger>
          <TabsTrigger value="search" className="text-xs">
            Search Entities
          </TabsTrigger>
        </TabsList>

        <TabsContent value="browse" className="mt-3">
          <label className="block text-xs text-gray-600 mb-1">
            Select an incident
          </label>
          <KgCombobox
            incidents={incidents}
            value={selectedNodeId}
            onSelect={onSelectNode}
            loading={incidentsLoading}
          />
        </TabsContent>

        <TabsContent value="search" className="mt-3 space-y-3">
          <div>
            <label className="block text-xs text-gray-600 mb-1">
              Entity type
            </label>
            <select
              className="w-full rounded-md border border-gray-300 px-2 py-1.5 text-sm bg-white"
              value={searchType}
              onChange={(e) => setSearchType(e.target.value)}
            >
              <option value="ALL">All types</option>
              {entityTypes.map((et) => (
                <option key={et.name} value={et.name}>
                  {et.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs text-gray-600 mb-1">
              Value pattern (regex)
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                className="flex-1 rounded-md border border-gray-300 px-2 py-1.5 text-sm"
                placeholder="e.g., forklift, fall.*"
                value={searchPattern}
                onChange={(e) => setSearchPattern(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSearchSubmit()}
              />
              <button
                className="px-3 py-1.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm flex items-center gap-1"
                onClick={handleSearchSubmit}
                disabled={searchLoading}
              >
                {searchLoading ? (
                  <Loader2 className="h-3.5 w-3.5 animate-spin" />
                ) : (
                  <Search className="h-3.5 w-3.5" />
                )}
              </button>
            </div>
          </div>

          {searchResults.length > 0 && (
            <div>
              <label className="block text-xs text-gray-600 mb-1">
                Results ({searchResults.length})
              </label>
              <div className="max-h-[200px] overflow-y-auto border border-gray-200 rounded-md">
                {searchResults.map((r) => (
                  <button
                    key={r.entity_id}
                    className={`w-full text-left px-2 py-1.5 text-xs hover:bg-blue-50 border-b border-gray-100 last:border-b-0 ${
                      selectedNodeId === r.entity_id
                        ? "bg-blue-50 font-medium"
                        : ""
                    }`}
                    onClick={() => onSelectNode(r.entity_id)}
                  >
                    <span className="text-gray-500">{r.entity_type}: </span>
                    <span className="text-gray-900">
                      {r.value.length > 50
                        ? r.value.substring(0, 47) + "..."
                        : r.value}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </TabsContent>
      </Tabs>

      {/* Divider */}
      <hr className="border-gray-200" />

      {/* Hop Depth */}
      <div>
        <label className="block text-xs text-gray-600 mb-2">Hop Depth</label>
        <div className="flex gap-2">
          {[1, 2].map((h) => (
            <button
              key={h}
              className={`flex-1 py-1.5 rounded-md text-sm font-medium border transition-colors ${
                hopDepth === h
                  ? "bg-blue-600 text-white border-blue-600"
                  : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50"
              }`}
              onClick={() => onHopDepthChange(h)}
            >
              {h}-hop
            </button>
          ))}
        </div>
      </div>

      {/* Entity Type Filter */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <label className="text-xs text-gray-600">Entity Type Filter</label>
          <button
            className="text-xs text-blue-600 hover:underline"
            onClick={() =>
              onEntityTypeFilterChange(
                allSelected ? [] : entityTypes.map((et) => et.name),
              )
            }
          >
            {allSelected ? "Clear all" : "Select all"}
          </button>
        </div>
        <div className="space-y-2">
          {entityTypes.map((et) => (
            <label
              key={et.name}
              className="flex items-center gap-2 cursor-pointer"
            >
              <Checkbox
                checked={entityTypeFilter.includes(et.name)}
                onCheckedChange={() => handleToggleEntityType(et.name)}
              />
              <span
                className="inline-block h-2.5 w-2.5 rounded-full"
                style={{ backgroundColor: et.color }}
              />
              <span className="text-sm text-gray-700">{et.label}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Explore Button */}
      <button
        className="w-full py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium text-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        onClick={onExplore}
        disabled={!selectedNodeId || exploring}
      >
        {exploring ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" />
            Building subgraph...
          </>
        ) : (
          "Explore"
        )}
      </button>
    </Card>
  );
}
