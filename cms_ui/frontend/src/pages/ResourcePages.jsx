import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";
import { Shell } from "../components/Shell";
import { PreviewPanel } from "../components/PreviewPanel";

const RESOURCE_CONFIG = {
  glossary: {
    listPath: "/glossary/?limit=100",
    itemPath: (id) => `/glossary/${id}`,
    createPath: "/glossary/",
    pushPath: (id) => `/glossary/${id}/push`,
    labelField: "term",
    title: "Glossary",
    fields: [
      { key: "term", label: "Term", type: "text", required: true },
      { key: "handle", label: "Handle", type: "text" },
      { key: "definition", label: "Definition (HTML)", type: "textarea" },
      { key: "locale_code", label: "Locale code", type: "text", placeholder: "en" },
      { key: "seo_title", label: "SEO title", type: "text" },
      { key: "search_description", label: "SEO description", type: "textarea" },
      { key: "sync_enabled", label: "Sync enabled", type: "checkbox" },
    ],
  },
  products: {
    listPath: "/products/?limit=100",
    itemPath: (id) => `/products/${id}`,
    createPath: "/products/",
    pushPath: (id) => `/products/${id}/push`,
    labelField: "title",
    title: "Products",
    fields: [
      { key: "title", label: "Title", type: "text", required: true },
      { key: "handle", label: "Handle", type: "text" },
      { key: "vendor", label: "Vendor", type: "text" },
      { key: "product_type", label: "Product type", type: "text" },
      { key: "seo_title", label: "SEO title", type: "text" },
      { key: "search_description", label: "SEO description", type: "textarea" },
      { key: "sync_enabled", label: "Sync enabled", type: "checkbox" },
    ],
  },
  collections: {
    listPath: "/collections/?limit=100",
    itemPath: (id) => `/collections/${id}`,
    createPath: "/collections/",
    pushPath: (id) => `/collections/${id}/push`,
    labelField: "title",
    title: "Collections",
    fields: [
      { key: "title", label: "Title", type: "text", required: true },
      { key: "handle", label: "Handle", type: "text" },
      { key: "seo_title", label: "SEO title", type: "text" },
      { key: "search_description", label: "SEO description", type: "textarea" },
      { key: "sync_enabled", label: "Sync enabled", type: "checkbox" },
    ],
  },
  blogs: {
    listPath: "/blogs/?limit=100",
    itemPath: (id) => `/blogs/${id}`,
    createPath: "/blogs/",
    pushPath: (id) => `/blogs/${id}/push`,
    labelField: "title",
    title: "Blogs",
    fields: [
      { key: "title", label: "Title", type: "text", required: true },
      { key: "handle", label: "Handle", type: "text" },
      { key: "sync_enabled", label: "Sync enabled", type: "checkbox" },
    ],
  },
  articles: {
    listPath: "/articles/?limit=100",
    itemPath: (id) => `/articles/${id}`,
    createPath: "/articles/",
    pushPath: (id) => `/articles/${id}/push`,
    labelField: "title",
    title: "Articles",
    fields: [
      { key: "title", label: "Title", type: "text", required: true },
      { key: "handle", label: "Handle", type: "text" },
      { key: "seo_title", label: "SEO title", type: "text" },
      { key: "search_description", label: "SEO description", type: "textarea" },
      { key: "sync_enabled", label: "Sync enabled", type: "checkbox" },
    ],
  },
  locations: {
    listPath: "/locations/?limit=100",
    itemPath: (id) => `/locations/${id}`,
    createPath: "/locations/",
    pushPath: (id) => `/locations/${id}/push`,
    labelField: "title",
    title: "Locations",
    fields: [
      { key: "title", label: "Title", type: "text", required: true },
      { key: "handle", label: "Handle", type: "text" },
      { key: "city", label: "City", type: "text" },
      { key: "seo_title", label: "SEO title", type: "text" },
      { key: "search_description", label: "SEO description", type: "textarea" },
      { key: "sync_enabled", label: "Sync enabled", type: "checkbox" },
    ],
  },
};

export function ResourceList({ resource }) {
  const cfg = RESOURCE_CONFIG[resource];
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    api(cfg.listPath)
      .then((data) => {
        if (!cancelled) setItems(Array.isArray(data) ? data : []);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [resource, cfg.listPath]);

  return (
    <Shell>
      <div className="page-head">
        <h1>{cfg.title}</h1>
        <Link className="btn" to={`/${resource}/new`}>
          Nuevo
        </Link>
      </div>
      {error && <p className="error">{error}</p>}
      {loading ? (
        <p>Cargando…</p>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Handle</th>
              <th>Live</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item[cfg.labelField] || item.title}</td>
                <td>{item.handle}</td>
                <td>{item.live ? "yes" : "draft"}</td>
                <td>
                  <Link to={`/${resource}/${item.id}`}>Editar</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Shell>
  );
}

function emptyForm(fields) {
  const data = {};
  fields.forEach((f) => {
    data[f.key] = f.type === "checkbox" ? true : "";
  });
  return data;
}

export function ResourceDetail({ resource }) {
  const { id } = useParams();
  const isNew = id === "new";
  const cfg = RESOURCE_CONFIG[resource];
  const [form, setForm] = useState(() => emptyForm(cfg.fields));
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [saving, setSaving] = useState(false);
  const numericId = isNew ? null : Number(id);

  useEffect(() => {
    if (isNew) {
      setForm(emptyForm(cfg.fields));
      return;
    }
    let cancelled = false;
    api(cfg.itemPath(id))
      .then((data) => {
        if (cancelled) return;
        const next = emptyForm(cfg.fields);
        cfg.fields.forEach((f) => {
          if (data[f.key] !== undefined && data[f.key] !== null) {
            next[f.key] = data[f.key];
          }
        });
        setForm(next);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      });
    return () => {
      cancelled = true;
    };
  }, [id, isNew, resource, cfg]);

  function updateField(key, value) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  async function save({ publish = false } = {}) {
    setSaving(true);
    setError("");
    setMessage("");
    try {
      const payload = { ...form, publish };
      Object.keys(payload).forEach((k) => {
        if (payload[k] === "") delete payload[k];
      });
      if (isNew) {
        const created = await api(cfg.createPath, {
          method: "POST",
          body: JSON.stringify(payload),
        });
        setMessage("Creado");
        window.location.hash = `#/${resource}/${created.id}`;
      } else {
        await api(cfg.itemPath(id), {
          method: "PATCH",
          body: JSON.stringify(payload),
        });
        setMessage(publish ? "Publicado" : "Borrador guardado");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  async function push() {
    if (!numericId) return;
    setSaving(true);
    setError("");
    try {
      const result = await api(cfg.pushPath(id), { method: "POST", body: "{}" });
      setMessage(result?.message || "Push OK");
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <Shell>
      <div className="page-head">
        <h1>
          {cfg.title}: {isNew ? "nuevo" : `#${id}`}
        </h1>
        <Link to={`/${resource}`}>← Volver</Link>
      </div>
      {error && <p className="error">{error}</p>}
      {message && <p className="ok">{message}</p>}
      <form
        className="edit-form"
        onSubmit={(e) => {
          e.preventDefault();
          save({ publish: false });
        }}
      >
        {cfg.fields.map((f) => (
          <label key={f.key} className="field">
            <span>{f.label}</span>
            {f.type === "textarea" ? (
              <textarea
                value={form[f.key] ?? ""}
                onChange={(e) => updateField(f.key, e.target.value)}
                rows={6}
              />
            ) : f.type === "checkbox" ? (
              <input
                type="checkbox"
                checked={Boolean(form[f.key])}
                onChange={(e) => updateField(f.key, e.target.checked)}
              />
            ) : (
              <input
                type="text"
                value={form[f.key] ?? ""}
                placeholder={f.placeholder || ""}
                required={Boolean(f.required)}
                onChange={(e) => updateField(f.key, e.target.value)}
              />
            )}
          </label>
        ))}
        <div className="cta-row">
          <button className="btn" type="submit" disabled={saving}>
            Guardar borrador
          </button>
          <button
            className="btn secondary"
            type="button"
            disabled={saving}
            onClick={() => save({ publish: true })}
          >
            Publicar
          </button>
          {!isNew && (
            <button className="btn secondary" type="button" disabled={saving} onClick={push}>
              Push a Shopify
            </button>
          )}
        </div>
      </form>
      {!isNew && <PreviewPanel resource={resource} id={numericId} />}
    </Shell>
  );
}

export { RESOURCE_CONFIG };
