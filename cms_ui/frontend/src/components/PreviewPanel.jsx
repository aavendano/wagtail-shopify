import React, { useState } from "react";
import { previewUrl } from "../api";

export function PreviewPanel({ resource, id }) {
  const [open, setOpen] = useState(false);
  if (!id) return null;
  const src = previewUrl(resource, id);

  return (
    <div className="preview-panel">
      <button type="button" className="btn secondary" onClick={() => setOpen((v) => !v)}>
        {open ? "Ocultar preview" : "Previsualizar"}
      </button>
      {open && (
        <iframe title="preview" className="preview-frame" src={src} />
      )}
    </div>
  );
}
