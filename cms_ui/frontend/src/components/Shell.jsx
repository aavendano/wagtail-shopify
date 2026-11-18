import React, { useCallback, useState } from "react";
import { Frame, Navigation, TopBar } from "@shopify/polaris";
import { useLocation, useNavigate } from "react-router-dom";
import { getBootstrap } from "../api";
import { useI18n } from "../i18n/I18nProvider";
import { LanguageSwitcher } from "./LanguageSwitcher";

export function Shell({ children }) {
  const boot = getBootstrap();
  const resources = boot.resources || [];
  const location = useLocation();
  const navigate = useNavigate();
  const { t } = useI18n();
  const [mobileNavActive, setMobileNavActive] = useState(false);
  const [userMenuActive, setUserMenuActive] = useState(false);

  const toggleMobileNav = useCallback(
    () => setMobileNavActive((active) => !active),
    [],
  );

  const toggleUserMenu = useCallback(
    () => setUserMenuActive((active) => !active),
    [],
  );

  const userMenuActions = boot.user
    ? [{ items: [{ content: boot.user.username, disabled: true }] }]
    : [
        {
          items: [
            {
              content: t("nav.login"),
              url: boot.loginUrl || "/admin-django/login/?next=/cms/",
            },
          ],
        },
      ];

  const topBarMarkup = (
    <TopBar
      showNavigationToggle
      userMenu={
        <TopBar.UserMenu
          actions={userMenuActions}
          name={boot.user ? boot.user.username : t("nav.guest")}
          initials={
            boot.user
              ? boot.user.username.slice(0, 2).toUpperCase()
              : "?"
          }
          open={userMenuActive}
          onToggle={toggleUserMenu}
        />
      }
      onNavigationToggle={toggleMobileNav}
      secondaryMenu={<LanguageSwitcher compact />}
    />
  );

  const navItems = [
    {
      label: t("nav.home"),
      url: "#/",
      selected: location.pathname === "/",
      onClick: () => {
        navigate("/");
        setMobileNavActive(false);
      },
    },
    ...resources.map((r) => ({
      label: t(`resource.${r.key}`) !== `resource.${r.key}` ? t(`resource.${r.key}`) : r.label,
      url: `#${r.path}`,
      selected:
        location.pathname === r.path ||
        location.pathname.startsWith(`${r.path}/`),
      onClick: () => {
        navigate(r.path);
        setMobileNavActive(false);
      },
    })),
  ];

  const navigationMarkup = (
    <Navigation location={location.pathname}>
      <Navigation.Section title={t("nav.cms")} items={navItems} />
    </Navigation>
  );

  return (
    <Frame
      topBar={topBarMarkup}
      navigation={navigationMarkup}
      showMobileNavigation={mobileNavActive}
      onNavigationDismiss={toggleMobileNav}
    >
      {children}
    </Frame>
  );
}
