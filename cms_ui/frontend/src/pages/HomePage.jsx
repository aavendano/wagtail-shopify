import React from "react";
import { BlockStack, Button, ButtonGroup, Card, Layout, Page, Text } from "@shopify/polaris";
import { useNavigate } from "react-router-dom";
import { getBootstrap } from "../api";
import { Shell } from "../components/Shell";
import { useI18n } from "../i18n/I18nProvider";

export function HomePage() {
  const boot = getBootstrap();
  const navigate = useNavigate();
  const { t } = useI18n();

  return (
    <Shell>
      <Page title={t("home.title")}>
        <Layout>
          <Layout.Section>
            <Card>
              <BlockStack gap="400">
                <Text as="p" variant="bodyMd">
                  {t("home.body", { apiBase: boot.apiBase || "/api/v1" })}
                </Text>
                <ButtonGroup>
                  {(boot.resources || []).map((r) => (
                    <Button key={r.key} onClick={() => navigate(r.path)}>
                      {t(`resource.${r.key}`) !== `resource.${r.key}`
                        ? t(`resource.${r.key}`)
                        : r.label}
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
