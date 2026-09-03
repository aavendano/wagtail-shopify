import React from "react";
import { Link } from "react-router-dom";
import { getBootstrap } from "../api";
import { Shell } from "../components/Shell";

export function HomePage() {
  const boot = getBootstrap();
  return (
    <Shell>
      <section className="hero-block">
        <h1>CMS editorial</h1>
        <p>
          Edita contenido Wagtail y publícalo a Shopify. La API en{" "}
          <code>{boot.apiBase || "/api/v1"}</code> alimenta esta UI, agentes y headless.
        </p>
        <div className="cta-row">
          {(boot.resources || []).map((r) => (
            <Link key={r.key} className="btn" to={r.path}>
              {r.label}
            </Link>
          ))}
        </div>
      </section>
    </Shell>
  );
}
