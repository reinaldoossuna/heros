/* prettier-ignore-start */

/* eslint-disable */

// @ts-nocheck

// noinspection JSUnusedGlobalSymbols

// This file is auto-generated by TanStack Router

// Import Routes

import { Route as rootRoute } from './routes/__root'
import { Route as LayoutImport } from './routes/_layout'
import { Route as LayoutIndexImport } from './routes/_layout/index'
import { Route as LayoutLinigrafosImport } from './routes/_layout/linigrafos'
import { Route as LayoutDownloadImport } from './routes/_layout/download'
import { Route as LayoutAboutImport } from './routes/_layout/about'
import { Route as LayoutMetereologiaImport } from './routes/_layout/Metereologia'

// Create/Update Routes

const LayoutRoute = LayoutImport.update({
  id: '/_layout',
  getParentRoute: () => rootRoute,
} as any)

const LayoutIndexRoute = LayoutIndexImport.update({
  path: '/',
  getParentRoute: () => LayoutRoute,
} as any)

const LayoutLinigrafosRoute = LayoutLinigrafosImport.update({
  path: '/linigrafos',
  getParentRoute: () => LayoutRoute,
} as any)

const LayoutDownloadRoute = LayoutDownloadImport.update({
  path: '/download',
  getParentRoute: () => LayoutRoute,
} as any)

const LayoutAboutRoute = LayoutAboutImport.update({
  path: '/about',
  getParentRoute: () => LayoutRoute,
} as any)

const LayoutMetereologiaRoute = LayoutMetereologiaImport.update({
  path: '/Metereologia',
  getParentRoute: () => LayoutRoute,
} as any)

// Populate the FileRoutesByPath interface

declare module '@tanstack/react-router' {
  interface FileRoutesByPath {
    '/_layout': {
      preLoaderRoute: typeof LayoutImport
      parentRoute: typeof rootRoute
    }
    '/_layout/Metereologia': {
      preLoaderRoute: typeof LayoutMetereologiaImport
      parentRoute: typeof LayoutImport
    }
    '/_layout/about': {
      preLoaderRoute: typeof LayoutAboutImport
      parentRoute: typeof LayoutImport
    }
    '/_layout/download': {
      preLoaderRoute: typeof LayoutDownloadImport
      parentRoute: typeof LayoutImport
    }
    '/_layout/linigrafos': {
      preLoaderRoute: typeof LayoutLinigrafosImport
      parentRoute: typeof LayoutImport
    }
    '/_layout/': {
      preLoaderRoute: typeof LayoutIndexImport
      parentRoute: typeof LayoutImport
    }
  }
}

// Create and export the route tree

export const routeTree = rootRoute.addChildren([
  LayoutRoute.addChildren([
    LayoutMetereologiaRoute,
    LayoutAboutRoute,
    LayoutDownloadRoute,
    LayoutLinigrafosRoute,
    LayoutIndexRoute,
  ]),
])

/* prettier-ignore-end */
