import type {
  IncidentListResponse,
  EntityTypeListResponse,
  EntitySearchResponse,
  SubgraphResponse,
} from "../types/kg";

const API_BASE = "/api/kg";

async function fetchJson<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`API error ${res.status}: ${detail}`);
  }
  return res.json();
}

export function fetchIncidents(): Promise<IncidentListResponse> {
  return fetchJson(`${API_BASE}/incidents`);
}

export function fetchEntityTypes(): Promise<EntityTypeListResponse> {
  return fetchJson(`${API_BASE}/entity-types`);
}

export function searchEntities(params: {
  entity_type?: string;
  value_pattern: string;
  max_results?: number;
}): Promise<EntitySearchResponse> {
  const qs = new URLSearchParams();
  if (params.entity_type) qs.set("entity_type", params.entity_type);
  qs.set("value_pattern", params.value_pattern);
  if (params.max_results) qs.set("max_results", String(params.max_results));
  return fetchJson(`${API_BASE}/search?${qs}`);
}

export function fetchSubgraph(params: {
  node_id: string;
  hops?: number;
  entity_type_filter?: string[];
}): Promise<SubgraphResponse> {
  const qs = new URLSearchParams();
  qs.set("node_id", params.node_id);
  qs.set("hops", String(params.hops ?? 1));
  if (params.entity_type_filter) {
    for (const et of params.entity_type_filter) {
      qs.append("entity_type_filter", et);
    }
  }
  return fetchJson(`${API_BASE}/subgraph?${qs}`);
}
