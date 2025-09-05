import { Box, Heading} from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/_layout/about")({
	component: AboutComponent,
});

function AboutComponent() {
	return (

		<Box maxH={"100vh"} pt={12} m={4}>
			<Heading size={"2xl"}>
				About
			</Heading>
		</Box>
	);
}
