import React from "react";
import { BlockStack, Button, ButtonGroup, Card, Layout, Page, Text } from "@shopify/polaris";
import { useNavigate } from "react-router-dom";
import { getBootstrap } from "../api";
import { Shell } from "../components/Shell";

export function HomePage() {
  const boot = getBootstrap();
  const navigate = useNavigate();

  return (
    <Shell>
      <Page title="CMS editorial">
        <Layout>
          <Layout.Section>
            <Card>
              <BlockStack gap="400">
                <Text as="p" variant="bodyMd">
                  Edita contenido Wagtail y publícalo a Shopify. La API en{" "}
                  <Text as="span" fontWeight="semibold">
                    {boot.apiBase || "/api/v1"}
                  </Text>{" "}
                  alimenta esta UI, agentes y headless.
                </Text>
                <ButtonGroup>
                  {(boot.resources || []).map((r) => (
                    <Button key={r.key} onClick={() => navigate(r.path)}>
                      {r.label}
                    </Button>
                  ))}
                </ButtonGroup>
              </BlockStack>
            </Card>
          </Layout.Section>
        </Layout>
      </Page>
    </Shell>
  );
}
