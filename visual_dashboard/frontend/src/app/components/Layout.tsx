import { useRef, useEffect, useState } from "react";
import { Outlet } from "react-router";
import {
  Activity,
  Search,
  Clock,
  FileDown,
  Loader2,
  Sparkles,
  X,
} from "lucide-react";
import { Card } from "./ui/card";
import { useQuery } from "../context/QueryContext";
import { exportNLQPdf } from "../api/kgApi";
import { toast } from "sonner";

const SUGGESTED_QUERIES = [
  "What equipment is most linked to near misses?",
  "Which sites show recurring confined space hazards?",
  "Trend analysis for LOTO deviations this quarter",
  "High-severity incidents involving temporary work at height",
];

export default function Layout() {
  const {
    query,
    setQuery,
    isLoading,
    error,
    result,
    runQuery,
    clearResult,
    recentQueries,
    isDropdownOpen,
    setIsDropdownOpen,
  } = useQuery();
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const handleSearch = () => {
    if (query.trim()) {
      runQuery();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSearch();
    }
    if (e.key === "Escape") {
      setIsDropdownOpen(false);
    }
  };

  const handleSuggestionClick = (q: string) => {
    setQuery(q);
    runQuery(q);
  };

  const [isExporting, setIsExporting] = useState(false);

  const answerTextRaw = result?.result_summary?.trim() ?? "";
  const answerText =
    answerTextRaw.length > 0 ? answerTextRaw : (result?.summary?.[0] ?? "").trim();
  const supportingBullets = (result?.summary ?? []).filter((b) => {
    const t = b.trim();
    if (!t) return false;
    if (!answerText) return true;
    const a = answerText.trim();
    return t !== a && t !== a.replace(/\.$/, "");
  });

  const handleExportPdf = async () => {
    if (!result) return;
    setIsExporting(true);
    try {
      const blob = await exportNLQPdf({
        title: result.title,
        original_query: result.original_query,
        summary: result.summary,
        referenced_reports: result.referenced_reports,
      });
      const url = URL.createObjectURL(blob);
      window.open(url, "_blank");
      setTimeout(() => URL.revokeObjectURL(url), 60000);
    } catch (e) {
      const msg = e instanceof Error ? e.message : "PDF export failed";
      toast.error(msg);
    } finally {
      setIsExporting(false);
    }
  };

  const formatTimestamp = (ts: number) => {
    const d = new Date(ts);
    return (
      d.toLocaleDateString("en-US", { month: "short", day: "numeric" }) +
      ", " +
      d.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" })
    );
  };

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(e.target as Node)
      ) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [setIsDropdownOpen]);

  // Show error toast
  useEffect(() => {
    if (error) {
      toast.error(error);
    }
  }, [error]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="font-semibold text-gray-900">
                  Safety Analytics Platform
                </h1>
                <p className="text-sm text-gray-500">
                  TechnipFMC Industrial Safety
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Persistent Natural Language Query Section */}
      <div className="bg-white border-b border-gray-200">
        <div className="px-6 py-4 max-w-[1800px] mx-auto">
          <Card className="p-6 shadow-sm border-gray-200">
            <div className="flex items-center gap-3 mb-2">
              <Search className="w-5 h-5 text-blue-600" />
              <label className="font-medium text-gray-900">
                Natural Language Query
              </label>
            </div>

            {/* Search bar + dropdown wrapper */}
            <div className="relative" ref={dropdownRef}>
              <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onFocus={() => !result && setIsDropdownOpen(true)}
                onKeyDown={handleKeyDown}
                placeholder="Ask a safety question (e.g., What equipment is most linked to near misses?)"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder:text-gray-400"
                disabled={isLoading}
              />
              <button
                onClick={handleSearch}
                disabled={isLoading || !query.trim()}
                className="absolute right-2 top-1/2 -translate-y-1/2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50"
              >
                {isLoading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  "Search"
                )}
              </button>

              {/* Dropdown: Recent + Suggested Queries */}
              {isDropdownOpen && !isLoading && !result && (
                <div className="absolute z-50 left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-[400px] overflow-y-auto">
                  {/* Recent Queries */}
                  <div className="p-4 border-b border-gray-100">
                    <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                      Recent Queries
                    </h3>
                    {recentQueries.length === 0 ? (
                      <p className="text-sm text-gray-400">
                        No recent searches yet.
                      </p>
                    ) : (
                      <div className="space-y-1">
                        {recentQueries.map((rq, i) => (
                          <button
                            key={i}
                            onClick={() => handleSuggestionClick(rq.query)}
                            className="w-full text-left px-3 py-2 rounded-md hover:bg-gray-50 flex items-start gap-3"
                          >
                            <Clock className="w-4 h-4 text-gray-400 mt-0.5 shrink-0" />
                            <div>
                              <p className="text-sm text-gray-900">
                                {rq.query}
                              </p>
                              <p className="text-xs text-gray-400">
                                {formatTimestamp(rq.timestamp)}
                              </p>
                            </div>
                          </button>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Suggested Queries */}
                  <div className="p-4">
                    <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                      Suggested Queries
                    </h3>
                    <div className="space-y-1">
                      {SUGGESTED_QUERIES.map((sq, i) => (
                        <button
                          key={i}
                          onClick={() => handleSuggestionClick(sq)}
                          className="w-full text-left px-3 py-2 rounded-md hover:bg-gray-50 text-sm text-gray-700"
                        >
                          {sq}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Loading State */}
            {isLoading && (
              <div className="mt-4 flex items-center gap-3 text-blue-600">
                <Loader2 className="w-5 h-5 animate-spin" />
                <span className="text-sm">
                  Analyzing your query against the knowledge graph...
                </span>
              </div>
            )}
          </Card>

          {/* Results Panel (outside the search Card, below it) */}
          {result && !isLoading && (
            <Card className="mt-4 p-6 border-l-4 border-l-blue-600 shadow-sm">
              {/* Title row */}
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3 min-w-0">
                  <Sparkles className="w-6 h-6 text-blue-600 mt-1 shrink-0" />
                  <div className="min-w-0">
                    <h2 className="text-lg font-semibold text-gray-900">
                      {result.title}
                    </h2>
                    <p className="text-sm text-gray-500 mt-0.5">
                      &ldquo;{result.original_query}&rdquo;
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2 shrink-0 ml-4">
                  <button
                    onClick={handleExportPdf}
                    disabled={isExporting}
                    className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50"
                  >
                    {isExporting ? (
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    ) : (
                      <FileDown className="w-3.5 h-3.5" />
                    )}
                    {isExporting ? "Exporting..." : "Export to PDF"}
                  </button>
                  <button
                    onClick={clearResult}
                    className="p-1.5 text-gray-400 hover:text-gray-600 rounded-md hover:bg-gray-50"
                    title="Dismiss results"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Low confidence warning */}
              {result.confidence < 0.7 && result.clarification && (
                <div className="mt-3 px-3 py-2 bg-amber-50 border border-amber-200 rounded text-sm text-amber-800">
                  Low confidence ({(result.confidence * 100).toFixed(0)}%):{" "}
                  {result.clarification}
                </div>
              )}

              {/* Answer (put the most important thing first) */}
              {answerText && (
                <div className="mt-4 rounded-lg border border-blue-100 bg-blue-50 px-4 py-3">
                  <h3 className="text-xs font-semibold text-blue-900 uppercase tracking-wide mb-1">
                    Answer
                  </h3>
                  <p className="text-sm text-blue-950 leading-relaxed">
                    {answerText}
                  </p>
                </div>
              )}

              {/* Supporting summary bullets */}
              {supportingBullets.length > 0 && (
                <div className="mt-4">
                  <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                    Key points
                  </h3>
                  <ul className="space-y-1.5">
                    {supportingBullets.map((bullet, i) => (
                      <li
                        key={i}
                        className="flex items-start gap-2 text-sm text-gray-700"
                      >
                        <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-gray-400 shrink-0" />
                        {bullet}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Referenced Safety Reports */}
              {result.referenced_reports.length > 0 && (
                <div className="mt-4">
                  <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                    Referenced Safety Reports
                  </h3>
                  <div className="flex flex-wrap gap-x-6 gap-y-1">
                    {result.referenced_reports.map((report) => (
                      <span
                        key={report.incident_id}
                        className="text-sm text-blue-600"
                      >
                        SER-{report.incident_id}
                        {report.incident_type &&
                          ` \u2014 ${report.incident_type}`}
                        {report.description &&
                          ` \u2014 ${report.description}`}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </Card>
          )}
        </div>
      </div>

      {/* Main Content */}
      <main>
        <Outlet />
      </main>
    </div>
  );
}
