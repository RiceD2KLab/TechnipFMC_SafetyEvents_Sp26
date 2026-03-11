import { useState, useEffect, useCallback } from "react";
import type {
  IncidentOption,
  EntityTypeInfo,
  SubgraphResponse,
  EntitySearchResult,
} from "../types/kg";
import {
  fetchIncidents,
  fetchEntityTypes,
  searchEntities,
  fetchSubgraph,
} from "../api/kgApi";

export function useIncidents() {
  const [incidents, setIncidents] = useState<IncidentOption[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchIncidents()
      .then((data) => setIncidents(data.incidents))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return { incidents, loading, error };
}

export function useEntityTypes() {
  const [entityTypes, setEntityTypes] = useState<EntityTypeInfo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEntityTypes()
      .then((data) => setEntityTypes(data.entity_types))
      .finally(() => setLoading(false));
  }, []);

  return { entityTypes, loading };
}

export function useEntitySearch() {
  const [results, setResults] = useState<EntitySearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const search = useCallback(
    async (entityType: string | undefined, valuePattern: string) => {
      if (!valuePattern.trim()) {
        setResults([]);
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const data = await searchEntities({
          entity_type: entityType,
          value_pattern: valuePattern,
          max_results: 50,
        });
        setResults(data.results);
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : "Search failed");
        setResults([]);
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  return { results, loading, error, search };
}

export function useSubgraph() {
  const [data, setData] = useState<SubgraphResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(
    async (
      nodeId: string,
      hops: number,
      entityTypeFilter: string[] | undefined,
    ) => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetchSubgraph({
          node_id: nodeId,
          hops,
          entity_type_filter: entityTypeFilter,
        });
        setData(response);
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : "Failed to load subgraph");
        setData(null);
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  return { data, loading, error, load };
}
