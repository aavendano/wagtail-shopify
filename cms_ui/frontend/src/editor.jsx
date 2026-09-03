import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { Puck } from "@puckeditor/core";
import "@puckeditor/core/puck.css";
import "./editor.css";

const config = {
  components: {
    HeadingBlock: {
      label: "Heading",
      fields: {
        title: { type: "text" },
      },
      defaultProps: { title: "Heading" },
      render: ({ title }) => <h2>{title}</h2>,
    },
    TextBlock: {
      label: "Text",
      fields: {
        text: { type: "textarea" },
      },
      defaultProps: { text: "Text" },
      render: ({ text }) => <p>{text}</p>,
    },
    ResourceLink: {
      label: "Resource link",
      fields: {
        resource: {
          type: "select",
          options: [
            { label: "Glossary", value: "glossary" },
            { label: "Products", value: "products" },
            { label: "Collections", value: "collections" },
            { label: "Blogs", value: "blogs" },
            { label: "Articles", value: "articles" },
            { label: "Locations", value: "locations" },
          ],
        },
        label: { type: "text" },
      },
      defaultProps: { resource: "glossary", label: "Glossary" },
      render: ({ resource, label }) => (
        <a href={`#/${resource}`}>{label || resource}</a>
      ),
    },
  },
};

function EditorApp({ initialLayout }) {
  const [data, setData] = useState(
    initialLayout?.root
      ? initialLayout
      : { root: { props: {} }, content: initialLayout?.content || [] },
  );

  const onPublish = useMemo(
    () => (next) => {
      setData(next);
      const layoutInput = document.querySelector("#id_layout");
      if (layoutInput) {
        layoutInput.value = JSON.stringify(next);
        layoutInput.dispatchEvent(new Event("input", { bubbles: true }));
        layoutInput.dispatchEvent(new Event("change", { bubbles: true }));
      }
    },
    [],
  );

  return (
    <div style={{ height: "70vh", border: "1px solid #ccc" }}>
      <Puck config={config} data={data} onPublish={onPublish} />
    </div>
  );
}

function boot() {
  const el = document.getElementById("visual-editor-root");
  if (!el) return;
  let layout = {};
  try {
    layout = JSON.parse(el.dataset.layoutJson || "{}");
  } catch {
    layout = {};
  }
  createRoot(el).render(<EditorApp initialLayout={layout} />);
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", boot);
} else {
  boot();
}
