import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  Banner,
  BlockStack,
  Button,
  Card,
  Checkbox,
  FormLayout,
  IndexTable,
  InlineStack,
  Layout,
  Page,
  Spinner,
  Text,
  TextField,
} from "@shopify/polaris";
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
  const navigate = useNavigate();
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

  const rowMarkup = items.map((item, index) => (
    <IndexTable.Row id={String(item.id)} key={item.id} position={index}>
      <IndexTable.Cell>
        <Text as="span" variant="bodyMd">
          {item.id}
        </Text>
      </IndexTable.Cell>
      <IndexTable.Cell>
        {item[cfg.labelField] || item.title}
      </IndexTable.Cell>
      <IndexTable.Cell>{item.handle}</IndexTable.Cell>
      <IndexTable.Cell>{item.live ? "yes" : "draft"}</IndexTable.Cell>
      <IndexTable.Cell>
        <Button variant="plain" onClick={() => navigate(`/${resource}/${item.id}`)}>
          Editar
        </Button>
      </IndexTable.Cell>
    </IndexTable.Row>
  ));

  return (
    <Shell>
      <Page
        title={cfg.title}
        primaryAction={{
          content: "Nuevo",
          onAction: () => navigate(`/${resource}/new`),
        }}
      >
        <Layout>
          <Layout.Section>
            <BlockStack gap="400">
              {error ? (
                <Banner tone="critical" title="Error">
                  <p>{error}</p>
                </Banner>
              ) : null}
              {loading ? (
                <InlineStack align="center">
                  <Spinner accessibilityLabel="Cargando" size="large" />
                </InlineStack>
              ) : (
                <Card padding="0">
                  <IndexTable
                    resourceName={{ singular: "registro", plural: "registros" }}
                    itemCount={items.length}
                    headings={[
                      { title: "ID" },
                      { title: "Nombre" },
                      { title: "Handle" },
                      { title: "Live" },
                      { title: "" },
                    ]}
                    selectable={false}
                  >
                    {rowMarkup}
                  </IndexTable>
                </Card>
              )}
            </BlockStack>
          </Layout.Section>
        </Layout>
      </Page>
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
  const navigate = useNavigate();
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

  const secondaryActions = [
    {
      content: "Publicar",
      onAction: () => save({ publish: true }),
      loading: saving,
      disabled: saving,
    },
  ];

  if (!isNew) {
    secondaryActions.push({
      content: "Push a Shopify",
      onAction: push,
      loading: saving,
      disabled: saving,
    });
  }

  return (
    <Shell>
      <Page
        title={`${cfg.title}: ${isNew ? "nuevo" : `#${id}`}`}
        backAction={{ content: cfg.title, onAction: () => navigate(`/${resource}`) }}
        primaryAction={{
          content: "Guardar borrador",
          onAction: () => save({ publish: false }),
          loading: saving,
          disabled: saving,
        }}
        secondaryActions={secondaryActions}
      >
        <Layout>
          <Layout.Section>
            <BlockStack gap="400">
              {error ? (
                <Banner tone="critical" title="Error">
                  <p>{error}</p>
                </Banner>
              ) : null}
              {message ? (
                <Banner tone="success" title="Listo">
                  <p>{message}</p>
                </Banner>
              ) : null}
              <Card>
                <FormLayout>
                  {cfg.fields.map((f) =>
                    f.type === "textarea" ? (
                      <TextField
                        key={f.key}
                        label={f.label}
                        value={form[f.key] ?? ""}
                        onChange={(value) => updateField(f.key, value)}
                        multiline={6}
                        autoComplete="off"
                      />
                    ) : f.type === "checkbox" ? (
                      <Checkbox
                        key={f.key}
                        label={f.label}
                        checked={Boolean(form[f.key])}
                        onChange={(checked) => updateField(f.key, checked)}
                      />
                    ) : (
                      <TextField
                        key={f.key}
                        label={f.label}
                        value={form[f.key] ?? ""}
                        onChange={(value) => updateField(f.key, value)}
                        placeholder={f.placeholder || ""}
                        requiredIndicator={Boolean(f.required)}
                        autoComplete="off"
                      />
                    ),
                  )}
                </FormLayout>
              </Card>
              {!isNew ? <PreviewPanel resource={resource} id={numericId} /> : null}
            </BlockStack>
          </Layout.Section>
        </Layout>
      </Page>
    </Shell>
  );
}

export { RESOURCE_CONFIG };
