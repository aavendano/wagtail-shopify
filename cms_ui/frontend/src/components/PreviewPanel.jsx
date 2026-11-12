import React, { useState } from "react";
import { BlockStack, Button, Card, Text } from "@shopify/polaris";
import { previewUrl } from "../api";

export function PreviewPanel({ resource, id }) {
  const [open, setOpen] = useState(false);
  if (!id) return null;
  const src = previewUrl(resource, id);

  return (
    <Card>
      <BlockStack gap="300">
        <Text as="h2" variant="headingSm">
          Preview
        </Text>
        <Button onClick={() => setOpen((v) => !v)}>
          {open ? "Ocultar preview" : "Previsualizar"}
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
