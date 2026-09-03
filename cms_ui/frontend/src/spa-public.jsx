import React from "react";
import { createRoot } from "react-dom/client";
import { HashRouter, Routes, Route, Navigate } from "react-router-dom";
import { HomePage } from "./pages/HomePage";
import { ResourceList, ResourceDetail } from "./pages/ResourcePages";
import "./spa.css";

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/glossary" element={<ResourceList resource="glossary" />} />
        <Route path="/glossary/:id" element={<ResourceDetail resource="glossary" />} />
        <Route path="/products" element={<ResourceList resource="products" />} />
        <Route path="/products/:id" element={<ResourceDetail resource="products" />} />
        <Route path="/collections" element={<ResourceList resource="collections" />} />
        <Route path="/collections/:id" element={<ResourceDetail resource="collections" />} />
        <Route path="/blogs" element={<ResourceList resource="blogs" />} />
        <Route path="/blogs/:id" element={<ResourceDetail resource="blogs" />} />
        <Route path="/articles" element={<ResourceList resource="articles" />} />
        <Route path="/articles/:id" element={<ResourceDetail resource="articles" />} />
        <Route path="/locations" element={<ResourceList resource="locations" />} />
        <Route path="/locations/:id" element={<ResourceDetail resource="locations" />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </HashRouter>
  );
}

const root = document.getElementById("cms-spa-root");
if (root) {
  createRoot(root).render(<App />);
}
