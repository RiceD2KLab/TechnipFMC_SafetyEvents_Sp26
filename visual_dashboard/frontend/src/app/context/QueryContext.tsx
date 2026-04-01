import { createContext, useCallback, useContext, useState, ReactNode } from "react";

export interface SafetyReportRef {
  id: string;
  title: string;
  href: string;
}

export interface QueryInsight {
  query: string;
  header: string;
  summary: string[];
  reports: SafetyReportRef[];
}

export interface RecentQueryEntry {
  text: string;
  at: number;
}

function insightHeaderFromQuery(q: string): string {
  const lower = q.toLowerCase();
  if (lower.includes("near miss") || lower.includes("near-miss")) {
    return "Near-miss patterns and linked operational factors";
  }
  if (lower.includes("equipment") || lower.includes("machinery")) {
    return "Equipment-linked incident and observation themes";
  }
  if (lower.includes("confined")) {
    return "Confined space exposure and control effectiveness";
  }
  if (lower.includes("trend") || lower.includes("quarter")) {
    return "Temporal trend synthesis across reported events";
  }
  return "Cross-incident safety synthesis";
}

function buildMockInsight(queryText: string): QueryInsight {
  const q = queryText.trim();
  const header = insightHeaderFromQuery(q);
  return {
    query: q,
    header,
    summary: [
      "Graph-linked records show recurring coupling between procedural drift, equipment state, and environmental factors for questions in this category.",
      "Elevated co-occurrence was noted for barrier weaknesses and communication gaps during simultaneous operations in comparable historical windows.",
      "Prioritize verification of critical controls and documented pre-job risk review where the same equipment classes or work modes appear repeatedly.",
    ],
    reports: [
      {
        id: "SER-2024-0189",
        title: "Near miss — lifting assembly / sling integrity",
        href: "#report-SER-2024-0189",
      },
      {
        id: "SER-2024-0142",
        title: "Observation — temporary work at height controls",
        href: "#report-SER-2024-0142",
      },
      {
        id: "SER-2023-2091",
        title: "Incident summary — energized work boundary",
        href: "#report-SER-2023-2091",
      },
    ],
  };
}

function insightToPlainText(insight: QueryInsight): string {
  const lines = [
    insight.header,
    "",
    ...insight.summary.map((s) => `• ${s}`),
    "",
    "Referenced reports:",
    ...insight.reports.map((r) => `${r.id}: ${r.title} (${r.href})`),
  ];
  return lines.join("\n");
}

interface QueryContextType {
  query: string;
  setQuery: (query: string) => void;
  searchResults: string | null;
  setSearchResults: (results: string | null) => void;
  queryInsight: QueryInsight | null;
  setQueryInsight: (insight: QueryInsight | null) => void;
  recentQueries: RecentQueryEntry[];
  submitQuery: () => void;
  selectQueryText: (text: string) => void;
  insightPlainText: (insight: QueryInsight) => string;
}

const QueryContext = createContext<QueryContextType | undefined>(undefined);

export function QueryProvider({ children }: { children: ReactNode }) {
  const [query, setQuery] = useState("");
  const [searchResults, setSearchResults] = useState<string | null>(null);
  const [queryInsight, setQueryInsight] = useState<QueryInsight | null>(null);
  const [recentQueries, setRecentQueries] = useState<RecentQueryEntry[]>([]);

  const submitQuery = useCallback(() => {
    const q = query.trim();
    if (!q) return;
    setRecentQueries((prev) => {
      const withoutDup = prev.filter((e) => e.text.toLowerCase() !== q.toLowerCase());
      return [{ text: q, at: Date.now() }, ...withoutDup].slice(0, 5);
    });
    setQueryInsight(buildMockInsight(q));
    setSearchResults(`Searching for: "${q}"`);
  }, [query]);

  const selectQueryText = useCallback((text: string) => {
    setQuery(text);
  }, []);

  const value: QueryContextType = {
    query,
    setQuery,
    searchResults,
    setSearchResults,
    queryInsight,
    setQueryInsight,
    recentQueries,
    submitQuery,
    selectQueryText,
    insightPlainText: insightToPlainText,
  };

  return <QueryContext.Provider value={value}>{children}</QueryContext.Provider>;
}

export function useQuery() {
  const context = useContext(QueryContext);
  if (context === undefined) {
    throw new Error("useQuery must be used within a QueryProvider");
  }
  return context;
}
