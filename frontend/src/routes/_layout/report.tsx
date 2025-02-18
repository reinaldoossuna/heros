import { Box, Heading, Flex, Button, useColorModeValue, Textarea } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";

export const Route = createFileRoute("/_layout/report")({
	component: ReportComponent,
});


function ReportComponent() {
	const [text, setText] = useState<string | null>(null)
	const fgColor = useColorModeValue("ui.dark", "ui.light")
	const handleSubmit = () => {
		console.log(text)
	}
	return (

		<Box maxH={"100vh"} pt={12} m={4}>
			<Heading size={"2xl"} color={fgColor}>
				Report
			</Heading>

			<Flex margin={20} >
				<object type="application/pdf" data="http://localhost:4444" width="100%" height="500"></object>
				<form >
					<Textarea name="conclusion" onChange={setText(event?.target.value)} />
					<Button onClick={handleSubmit}>
					</Button>
				</form>
			</Flex>

		</Box>
	);
}
