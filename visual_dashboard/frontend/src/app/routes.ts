import { createBrowserRouter } from "react-router";
import Layout from "./components/Layout";
import MainDashboard from "./pages/MainDashboard";
import KnowledgeGraphReasoning from "./pages/KnowledgeGraphReasoning";
import DataExtractionQuality from "./pages/DataExtractionQuality";
import EventSimilarityDiscovery from "./pages/EventSimilarityDiscovery";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Layout,
    children: [
      { index: true, Component: MainDashboard },
      { path: "reasoning", Component: KnowledgeGraphReasoning },
      { path: "extraction", Component: DataExtractionQuality },
      { path: "similarity", Component: EventSimilarityDiscovery },
    ],
  },
]);
