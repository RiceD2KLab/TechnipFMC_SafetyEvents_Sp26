import {
  createContext,
  useContext,
  useState,
  useCallback,
  type ReactNode,
} from "react";
import type { NLQResponse, RecentQuery } from "../types/kg";
import { executeNLQuery } from "../api/kgApi";

const RECENT_QUERIES_KEY = "nlq_recent_queries";
const MAX_RECENT = 10;

interface QueryContextType {
  query: string;
  setQuery: (query: string) => void;

  isLoading: boolean;
  error: string | null;
  result: NLQResponse | null;
  runQuery: (q?: string) => Promise<void>;
  clearResult: () => void;

  recentQueries: RecentQuery[];
  clearRecentQueries: () => void;

  isDropdownOpen: boolean;
  setIsDropdownOpen: (open: boolean) => void;
}

const QueryContext = createContext<QueryContextType | undefined>(undefined);

function loadRecentQueries(): RecentQuery[] {
  try {
    const raw = localStorage.getItem(RECENT_QUERIES_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveRecentQueries(queries: RecentQuery[]) {
  localStorage.setItem(RECENT_QUERIES_KEY, JSON.stringify(queries));
}

export function QueryProvider({ children }: { children: ReactNode }) {
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<NLQResponse | null>(null);
  const [recentQueries, setRecentQueries] = useState<RecentQuery[]>(
    loadRecentQueries
  );
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const clearResult = useCallback(() => {
    setResult(null);
    setError(null);
  }, []);

  const clearRecentQueries = useCallback(() => {
    setRecentQueries([]);
    saveRecentQueries([]);
  }, []);

  const runQuery = useCallback(
    async (q?: string) => {
      const queryText = (q ?? query).trim();
      if (!queryText) return;

      setIsLoading(true);
      setError(null);
      setResult(null);
      setIsDropdownOpen(false);

      try {
        const response = await executeNLQuery(queryText);
        setResult(response);

        const newRecent: RecentQuery = {
          query: queryText,
          timestamp: Date.now(),
          title: response.title,
        };
        setRecentQueries((prev) => {
          const filtered = prev.filter((r) => r.query !== queryText);
          const updated = [newRecent, ...filtered].slice(0, MAX_RECENT);
          saveRecentQueries(updated);
          return updated;
        });
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : "Query failed";
        setError(msg);
      } finally {
        setIsLoading(false);
      }
    },
    [query]
  );

  return (
    <QueryContext.Provider
      value={{
        query,
        setQuery,
        isLoading,
        error,
        result,
        runQuery,
        clearResult,
        recentQueries,
        clearRecentQueries,
        isDropdownOpen,
        setIsDropdownOpen,
      }}
    >
      {children}
    </QueryContext.Provider>
  );
}

export function useQuery() {
  const context = useContext(QueryContext);
  if (context === undefined) {
    throw new Error("useQuery must be used within a QueryProvider");
  }
  return context;
}
