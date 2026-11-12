import React from "react";
import { AppProvider } from "@shopify/polaris";
import enTranslations from "@shopify/polaris/locales/en.json";
import "@shopify/polaris/build/esm/styles.css";

/**
 * Polaris shell for the CMS embedded in Shopify Admin (/cms/).
 * Public storefront pages use Wagtail templates, not this bundle.
 */
export function EmbeddedAppProvider({ children }) {
  return <AppProvider i18n={enTranslations}>{children}</AppProvider>;
}
