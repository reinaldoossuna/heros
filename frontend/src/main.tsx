import { ChakraProvider } from "@chakra-ui/react";
import { RouterProvider, createRouter } from "@tanstack/react-router";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import { routeTree } from "./routeTree.gen.ts";
import theme from "./theme.tsx";
import { client } from "./client/sdk.gen.ts";
import 'leaflet/dist/leaflet.css'

const queryClient = new QueryClient({
	defaultOptions: {
		queries: {
			staleTime: Infinity,
			gcTime: 1000 * 60 * 60 * 24
		}
	}
})

const router = createRouter({ routeTree });

client.setConfig({
	baseUrl: import.meta.env.VITE_API_URL
})

createRoot(document.getElementById("root")!).render(
	<StrictMode>
		<ChakraProvider theme={theme}>
			<QueryClientProvider client={queryClient}>
				<ReactQueryDevtools initialIsOpen={false} />
				<RouterProvider router={router} />
			</QueryClientProvider>
		</ChakraProvider>
	</StrictMode>,
);
