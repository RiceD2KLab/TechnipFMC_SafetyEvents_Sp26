import { useCallback, useEffect, useRef, useState } from "react";
import { Outlet, Link, useLocation } from "react-router";
import {
  Activity,
  BarChart3,
  Clock,
  Copy,
  GitBranch,
  Search,
  Share2,
  Sparkles,
} from "lucide-react";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { useQuery } from "../context/QueryContext";

const SUGGESTED_QUERIES = [
  "What equipment is most linked to near misses?",
  "Which sites show recurring confined space hazards?",
  "Trend analysis for LOTO deviations this quarter",
  "High-severity incidents involving temporary work at height",
];

function formatQueryTimestamp(at: number): string {
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(at));
}

export default function Layout() {
  const location = useLocation();
  const queryModuleRef = useRef<HTMLDivElement>(null);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [copyDone, setCopyDone] = useState(false);

  const {
    query,
    setQuery,
    queryInsight,
    submitQuery,
    recentQueries,
    selectQueryText,
    insightPlainText,
  } = useQuery();

  const navigation = [
    { name: "Dashboard", path: "/", icon: BarChart3 },
    { name: "Graph Reasoning", path: "/reasoning", icon: GitBranch },
    { name: "Data Extraction", path: "/extraction", icon: Search },
    { name: "Event Similarity", path: "/similarity", icon: Activity },
  ];

  useEffect(() => {
    function handlePointerDown(e: MouseEvent) {
      if (queryModuleRef.current && !queryModuleRef.current.contains(e.target as Node)) {
        setDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handlePointerDown);
    return () => document.removeEventListener("mousedown", handlePointerDown);
  }, []);

  const handleSearch = () => {
    submitQuery();
    setDropdownOpen(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSearch();
    }
    if (e.key === "Escape") {
      setDropdownOpen(false);
    }
  };

  const pickSuggestion = (text: string) => {
    selectQueryText(text);
    setDropdownOpen(false);
  };

  const pickRecent = (text: string) => {
    selectQueryText(text);
    setDropdownOpen(false);
  };

  const handleCopyInsight = useCallback(async () => {
    if (!queryInsight) return;
    const text = insightPlainText(queryInsight);
    try {
      await navigator.clipboard.writeText(text);
      setCopyDone(true);
      window.setTimeout(() => setCopyDone(false), 2000);
    } catch {
      setCopyDone(false);
    }
  }, [queryInsight, insightPlainText]);

  const handleShareInsight = useCallback(async () => {
    if (!queryInsight) return;
    const text = insightPlainText(queryInsight);
    const title = queryInsight.header;
    try {
      if (navigator.share) {
        await navigator.share({ title, text });
      } else {
        await navigator.clipboard.writeText(text);
        setCopyDone(true);
        window.setTimeout(() => setCopyDone(false), 2000);
      }
    } catch {
      /* user cancel or share unsupported */
    }
  }, [queryInsight, insightPlainText]);

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
                <h1 className="font-semibold text-gray-900">Safety Analytics Platform</h1>
                <p className="text-sm text-gray-500">TechnipFMC Industrial Safety</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="px-6">
          <div className="flex gap-1">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-2 px-4 py-3 border-b-2 transition-colors ${
                    isActive
                      ? "border-blue-600 text-blue-600"
                      : "border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="text-sm font-medium">{item.name}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Persistent Natural Language Query Section */}
      <div className="bg-white border-b border-gray-200">
        <div className="px-6 py-4 max-w-[1800px] mx-auto space-y-4">
          <Card className="p-6 shadow-sm border-gray-200">
            <div className="flex items-center gap-3 mb-2">
              <Search className="w-5 h-5 text-blue-600 shrink-0" aria-hidden />
              <label htmlFor="nl-query-input" className="font-medium text-gray-900">
                Natural Language Query
              </label>
            </div>
            <div ref={queryModuleRef} className="relative">
              <input
                id="nl-query-input"
                type="text"
                role="combobox"
                aria-expanded={dropdownOpen}
                aria-controls="query-management-dropdown"
                aria-autocomplete="list"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onFocus={() => setDropdownOpen(true)}
                onKeyDown={handleKeyDown}
                placeholder="Ask a safety question (e.g., What equipment is most linked to near misses?)"
                className="w-full pl-4 pr-[6.5rem] py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder:text-gray-400 text-base"
              />
              <button
                type="button"
                onClick={handleSearch}
                className="absolute right-2 top-1/2 -translate-y-1/2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Search
              </button>

              {dropdownOpen && (
                <div
                  id="query-management-dropdown"
                  role="listbox"
                  className="absolute left-0 right-0 top-full z-50 mt-2 rounded-lg border border-gray-200 bg-white shadow-lg ring-1 ring-black/5 overflow-hidden"
                  onMouseDown={(e) => e.preventDefault()}
                >
                  <div className="max-h-[min(22rem,70vh)] overflow-y-auto">
                    <div className="px-3 pt-3 pb-1">
                      <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
                        Recent queries
                      </p>
                    </div>
                    {recentQueries.length === 0 ? (
                      <p className="px-3 pb-3 text-sm text-gray-500">No recent searches yet.</p>
                    ) : (
                      <ul className="pb-2" aria-label="Recent queries">
                        {recentQueries.map((entry) => (
                          <li key={`${entry.text}-${entry.at}`}>
                            <button
                              type="button"
                              role="option"
                              onClick={() => pickRecent(entry.text)}
                              className="w-full text-left px-3 py-2.5 hover:bg-gray-50 flex gap-3 items-start border-t border-gray-100 first:border-t-0"
                            >
                              <Clock
                                className="w-4 h-4 text-gray-400 shrink-0 mt-0.5"
                                aria-hidden
                              />
                              <span className="min-w-0 flex-1">
                                <span className="block text-sm text-gray-900 leading-snug">
                                  {entry.text}
                                </span>
                                <span className="block text-xs text-gray-500 mt-0.5">
                                  {formatQueryTimestamp(entry.at)}
                                </span>
                              </span>
                            </button>
                          </li>
                        ))}
                      </ul>
                    )}
                    <div className="border-t border-gray-200 bg-gray-50/80 px-3 pt-3 pb-1">
                      <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
                        Suggested queries
                      </p>
                    </div>
                    <ul className="pb-2" aria-label="Suggested queries">
                      {SUGGESTED_QUERIES.map((suggestion) => (
                        <li key={suggestion}>
                          <button
                            type="button"
                            role="option"
                            onClick={() => pickSuggestion(suggestion)}
                            className="w-full text-left px-3 py-2.5 text-sm text-gray-800 hover:bg-white hover:text-blue-700 border-t border-gray-100"
                          >
                            {suggestion}
                          </button>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>
          </Card>

          {queryInsight && (
            <section
              aria-labelledby="query-insight-heading"
              className="rounded-xl border border-gray-200 bg-white shadow-md border-l-4 border-l-blue-600 overflow-hidden"
            >
              <div className="px-6 py-4 border-b border-gray-100 bg-gray-50/60 flex flex-wrap items-start justify-between gap-4">
                <div className="flex items-start gap-3 min-w-0">
                  <div className="p-2 rounded-lg bg-blue-100 text-blue-700 shrink-0">
                    <Sparkles className="w-5 h-5" aria-hidden />
                  </div>
                  <div className="min-w-0">
                    <h2
                      id="query-insight-heading"
                      className="text-lg font-semibold text-gray-900 leading-tight"
                    >
                      {queryInsight.header}
                    </h2>
                    <p className="text-sm text-gray-600 mt-1">
                      <span className="sr-only">Original question: </span>
                      <q className="not-italic text-gray-700">{queryInsight.query}</q>
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    className="border-gray-300 text-gray-800 hover:bg-gray-50"
                    onClick={handleCopyInsight}
                  >
                    <Copy className="w-4 h-4 mr-1.5" aria-hidden />
                    {copyDone ? "Copied" : "Copy"}
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    className="border-gray-300 text-gray-800 hover:bg-gray-50"
                    onClick={handleShareInsight}
                  >
                    <Share2 className="w-4 h-4 mr-1.5" aria-hidden />
                    Share
                  </Button>
                </div>
              </div>
              <div className="px-6 py-5">
                <h3 className="text-xs font-semibold uppercase tracking-wide text-gray-500 mb-3">
                  Summary
                </h3>
                <ul className="list-disc pl-5 space-y-2 text-gray-800 text-sm leading-relaxed">
                  {queryInsight.summary.map((point, i) => (
                    <li key={i}>{point}</li>
                  ))}
                </ul>
                <h3 className="text-xs font-semibold uppercase tracking-wide text-gray-500 mt-6 mb-2">
                  Referenced safety reports
                </h3>
                <ul className="flex flex-wrap gap-x-4 gap-y-2">
                  {queryInsight.reports.map((r) => (
                    <li key={r.id}>
                      <a
                        href={r.href}
                        className="text-sm text-blue-700 hover:text-blue-800 underline decoration-blue-200 hover:decoration-blue-600 underline-offset-2 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-0.5"
                      >
                        <span className="font-medium">{r.id}</span>
                        <span className="text-gray-600 font-normal"> — {r.title}</span>
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            </section>
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
