import type {
  IncidentListResponse,
  EntityTypeListResponse,
  EntitySearchResponse,
  SubgraphResponse,
  NLQResponse,
} from "../types/kg";

const API_BASE = "/api/kg";
const NLQ_BASE = "/api/nlq";

async function fetchJson<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`API error ${res.status}: ${detail}`);
  }
  return res.json();
}

async function postJson<T>(url: string, body: unknown): Promise<T> {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
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

export function executeNLQuery(query: string): Promise<NLQResponse> {
  return postJson(`${NLQ_BASE}/query`, { query });
}

export async function exportNLQPdf(data: {
  title: string;
  original_query: string;
  summary: string[];
  referenced_reports: { incident_id: string; incident_type: string | null; description: string | null }[];
}): Promise<Blob> {
  const res = await fetch(`${NLQ_BASE}/export-pdf`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`PDF export failed: ${detail}`);
  }
  return res.blob();
}
