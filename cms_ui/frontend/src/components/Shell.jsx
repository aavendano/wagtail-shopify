import React, { useCallback, useState } from "react";
import { Frame, Navigation, TopBar } from "@shopify/polaris";
import { useLocation, useNavigate } from "react-router-dom";
import { getBootstrap } from "../api";

export function Shell({ children }) {
  const boot = getBootstrap();
  const resources = boot.resources || [];
  const location = useLocation();
  const navigate = useNavigate();
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
              content: "Login",
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
          name={boot.user ? boot.user.username : "Guest"}
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
    />
  );

  const navItems = [
    {
      label: "Inicio",
      url: "#/",
      selected: location.pathname === "/",
      onClick: () => {
        navigate("/");
        setMobileNavActive(false);
      },
    },
    ...resources.map((r) => ({
      label: r.label,
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
      <Navigation.Section title="CMS" items={navItems} />
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
