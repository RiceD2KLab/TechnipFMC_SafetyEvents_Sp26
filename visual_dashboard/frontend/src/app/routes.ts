import { createBrowserRouter } from "react-router";
import Layout from "./components/Layout";
import KnowledgeGraphReasoning from "./pages/KnowledgeGraphReasoning";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Layout,
    children: [
      { index: true, Component: KnowledgeGraphReasoning },
    ],
  },
]);
