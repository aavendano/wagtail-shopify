import React from "react";
import { Link, NavLink } from "react-router-dom";
import { getBootstrap } from "../api";

export function Shell({ children }) {
  const boot = getBootstrap();
  const resources = boot.resources || [];

  return (
    <div className="cms-shell">
      <header className="cms-header">
        <div className="cms-brand">
          <Link to="/">CMS</Link>
        </div>
        <nav className="cms-nav">
          {resources.map((r) => (
            <NavLink key={r.key} to={r.path} className={({ isActive }) => (isActive ? "active" : undefined)}>
              {r.label}
            </NavLink>
          ))}
        </nav>
        <div className="cms-user">
          {boot.user ? (
            <span>{boot.user.username}</span>
          ) : (
            <a href={boot.loginUrl || "/admin-django/login/?next=/cms/"}>Login</a>
          )}
        </div>
      </header>
      <main className="cms-main">{children}</main>
    </div>
  );
}
