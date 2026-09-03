function csrfToken() {
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : "";
}

export function getBootstrap() {
  return window.__CMS_BOOTSTRAP__ || { apiBase: "/api/v1", resources: [] };
}

export async function api(path, options = {}) {
  const { apiBase } = getBootstrap();
  const headers = {
    Accept: "application/json",
    ...(options.headers || {}),
  };
  if (options.body && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }
  const method = (options.method || "GET").toUpperCase();
  if (method !== "GET" && method !== "HEAD") {
    headers["X-CSRFToken"] = csrfToken();
  }
  const res = await fetch(`${apiBase}${path}`, {
    credentials: "same-origin",
    ...options,
    headers,
  });
  if (res.status === 204) {
    return null;
  }
  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }
  if (!res.ok) {
    const detail = data?.detail || data?.message || res.statusText;
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return data;
}

export function previewUrl(resource, id) {
  const { apiBase } = getBootstrap();
  return `${apiBase}/${resource}/${id}/preview`;
}
