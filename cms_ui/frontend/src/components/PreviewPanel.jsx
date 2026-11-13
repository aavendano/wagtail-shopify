import React, { useState } from "react";
import { BlockStack, Button, Card, Text } from "@shopify/polaris";
import { previewUrl } from "../api";
import { useI18n } from "../i18n/I18nProvider";

export function PreviewPanel({ resource, id }) {
  const { t } = useI18n();
  const [open, setOpen] = useState(false);
  if (!id) return null;
  const src = previewUrl(resource, id);

  return (
    <Card>
      <BlockStack gap="300">
        <Text as="h2" variant="headingSm">
          {t("preview.title")}
        </Text>
        <Button onClick={() => setOpen((v) => !v)}>
          {open ? t("preview.hide") : t("preview.show")}
        </Button>
        {open ? (
          <iframe
            title="preview"
            src={src}
            style={{
              width: "100%",
              minHeight: "480px",
              border: "1px solid var(--p-color-border)",
              borderRadius: "var(--p-border-radius-200)",
            }}
          />
        ) : null}
      </BlockStack>
    </Card>
  );
}
