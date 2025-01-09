import { Outlet, createRootRoute } from "@tanstack/react-router";
import React from "react";

export const Route = createRootRoute({
    component: RootComponent,
});

const TanStackRouterDevtools =
    process.env.NODE_ENV === 'production'
    ? () => null // Render nothing in production
    : React.lazy(() =>
        // Lazy load in development
        import('@tanstack/router-devtools').then((res) => ({
          default: res.TanStackRouterDevtools,
          // For Embedded Mode
          // default: res.TanStackRouterDevtoolsPanel
        })),
      )

function RootComponent() {
    return (
        <>
            <Outlet />
            <TanStackRouterDevtools position="bottom-right" />
        </>
    );
}
