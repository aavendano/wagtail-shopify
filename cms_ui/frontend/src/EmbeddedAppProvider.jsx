import React from "react";
import { AppProvider } from "@shopify/polaris";
import enPolaris from "@shopify/polaris/locales/en.json";
import esPolaris from "@shopify/polaris/locales/es.json";
import frPolaris from "@shopify/polaris/locales/fr.json";
import "@shopify/polaris/build/esm/styles.css";
import { getBootstrap } from "./api";
import { I18nProvider, useI18n } from "./i18n/I18nProvider";

const POLARIS_BY_LANGUAGE = {
  "en-US": enPolaris,
  "en-CA": enPolaris,
  "es-US": esPolaris,
  "fr-CA": frPolaris,
};

function PolarisShell({ children }) {
  const { language } = useI18n();
  const polarisI18n = POLARIS_BY_LANGUAGE[language] || enPolaris;
  return <AppProvider i18n={polarisI18n}>{children}</AppProvider>;
}

/**
 * Polaris shell for the CMS embedded in Shopify Admin (/cms/).
 * Public storefront pages use Wagtail templates, not this bundle.
 */
export function EmbeddedAppProvider({ children }) {
  const boot = getBootstrap();
  const lang =
    typeof window !== "undefined"
      ? window.localStorage.getItem(boot.localeStorageKey || "cms_ui_locale") ||
        boot.language
      : boot.language;

  return (
    <I18nProvider key={lang}>
      <PolarisShell>{children}</PolarisShell>
    </I18nProvider>
  );
}
