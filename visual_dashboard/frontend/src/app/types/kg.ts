export interface GraphNode {
  id: string;
  entity_type: string;
  value: string;
  x: number;
  y: number;
  is_center: boolean;
  properties: Record<string, string | number>;
}

export interface GraphEdge {
  source: string;
  target: string;
  relation: string;
  confidence: number | null;
  source_type: string | null;
}

export interface SubgraphStats {
  node_count: number;
  edge_count: number;
  entity_type_counts: Record<string, number>;
  relation_type_counts: Record<string, number>;
}

export interface SubgraphResponse {
  nodes: GraphNode[];
  edges: GraphEdge[];
  stats: SubgraphStats;
  truncated: boolean;
  center_node_id: string;
}

export interface EntitySearchResult {
  entity_id: string;
  entity_type: string;
  value: string;
}

export interface EntitySearchResponse {
  results: EntitySearchResult[];
  total_count: number;
}

export interface IncidentOption {
  label: string;
  entity_id: string;
}

export interface IncidentListResponse {
  incidents: IncidentOption[];
}

export interface EntityTypeInfo {
  name: string;
  label: string;
  color: string;
}

export interface EntityTypeListResponse {
  entity_types: EntityTypeInfo[];
}
