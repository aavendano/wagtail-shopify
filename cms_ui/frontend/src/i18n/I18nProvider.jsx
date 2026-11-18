import React, { createContext, useCallback, useContext, useMemo, useState } from "react";
import { getBootstrap } from "../api";
import enUS from "./locales/en-US.json";
import esUS from "./locales/es-US.json";
import enCA from "./locales/en-CA.json";
import frCA from "./locales/fr-CA.json";

const CATALOGS = {
  "en-US": enUS,
  "es-US": esUS,
  "en-CA": { ...enUS, ...enCA },
  "fr-CA": { ...enUS, ...frCA },
};

const I18nContext = createContext({
  language: "en-US",
  t: (key) => key,
  setLanguage: async () => {},
  availableLocales: [],
});

function readStoredLanguage(storageKey) {
  try {
    return window.localStorage.getItem(storageKey) || "";
  } catch {
    return "";
  }
}

function resolveInitialLanguage(boot) {
  const storageKey = boot.localeStorageKey || "cms_ui_locale";
  const allowed = new Set((boot.availableLocales || []).map((l) => l.code));
  const stored = readStoredLanguage(storageKey);
  if (stored && allowed.has(stored)) {
    return stored;
  }
  if (boot.language && allowed.has(boot.language)) {
    return boot.language;
  }
  const first = (boot.availableLocales || [])[0];
  return first?.code || boot.language || "en-US";
}

export function I18nProvider({ children }) {
  const boot = getBootstrap();
  const [language, setLanguageState] = useState(() => resolveInitialLanguage(boot));

  const catalog = CATALOGS[language] || CATALOGS["en-US"] || enUS;

  const t = useCallback(
    (key, vars = {}) => {
      let text = catalog[key] ?? CATALOGS["en-US"][key] ?? key;
      Object.entries(vars).forEach(([k, v]) => {
        text = text.replaceAll(`{${k}}`, String(v));
      });
      return text;
    },
    [catalog],
  );

  const setLanguage = useCallback(
    async (code) => {
      const allowed = new Set((boot.availableLocales || []).map((l) => l.code));
      if (!allowed.has(code)) {
        return;
      }
      const url = boot.setLanguageUrl || "/cms/set-language/";
      const res = await fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "X-CSRFToken": document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/)?.[1]
            ? decodeURIComponent(
                document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/)[1],
              )
            : "",
        },
        body: JSON.stringify({ language: code }),
      });
      if (!res.ok) {
        throw new Error("Failed to set language");
      }
      try {
        window.localStorage.setItem(boot.localeStorageKey || "cms_ui_locale", code);
      } catch {
        /* ignore */
      }
      setLanguageState(code);
      window.location.reload();
    },
    [boot],
  );

  const value = useMemo(
    () => ({
      language,
      t,
      setLanguage,
      availableLocales: boot.availableLocales || [],
    }),
    [language, t, setLanguage, boot.availableLocales],
  );

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useI18n() {
  return useContext(I18nContext);
}

export function translateFieldLabel(t, key) {
  const map = {
    term: "fields.term",
    handle: "fields.handle",
    definition: "fields.definition",
    locale_code: "fields.localeCode",
    seo_title: "fields.seoTitle",
    search_description: "fields.seoDescription",
    sync_enabled: "fields.syncEnabled",
    title: "fields.title",
    vendor: "fields.vendor",
    product_type: "fields.productType",
    city: "fields.city",
  };
  return t(map[key] || key);
}

export function translateResourceTitle(t, resource) {
  return t(`resource.${resource}`);
}
