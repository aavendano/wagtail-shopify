import React, { useCallback } from "react";
import { Select } from "@shopify/polaris";
import { useI18n } from "../i18n/I18nProvider";

export function LanguageSwitcher({ compact = false }) {
  const { language, setLanguage, availableLocales, t } = useI18n();

  const options = availableLocales.map((loc) => ({
    label: loc.label || loc.code,
    value: loc.code,
  }));

  const onChange = useCallback(
    (value) => {
      if (value && value !== language) {
        setLanguage(value).catch(() => {});
      }
    },
    [language, setLanguage],
  );

  if (options.length < 2) {
    return null;
  }

  const select = (
    <Select
      label={compact ? undefined : t("nav.language")}
      labelHidden={compact}
      options={options}
      value={language}
      onChange={onChange}
    />
  );

  if (compact) {
    return <div style={{ minWidth: "10rem", padding: "0 0.5rem" }}>{select}</div>;
  }

  return <div style={{ padding: "0.75rem 1rem" }}>{select}</div>;
}
