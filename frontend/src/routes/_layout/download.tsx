import { Box, Heading, useColorModeValue } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/_layout/download")({
	component: DownloadComponent,
});

function DownloadComponent() {
	const fgColor = useColorModeValue("ui.dark", "ui.light")
	return (

		<Box maxH={"100vh"} pt={12} m={4}>
			<Heading size={"2xl"} color={fgColor}>
				Download Data
			</Heading>
		</Box>
	);
}
