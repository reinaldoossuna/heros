import { Container, Flex, useColorModeValue } from "@chakra-ui/react";
import { Outlet, createFileRoute } from "@tanstack/react-router";
import Sidebar from "../components/common/Sidebar"

export const Route = createFileRoute("/_layout")({
    component: Layout,
})

function Layout() {

    const bgColor = useColorModeValue("ui.light", "ui.dark")
    return (
        <Flex h="100vh" position="relative">
            <Sidebar />
            <Container maxW="full" bg={bgColor} overflow={"scroll"}>
                <Outlet />
            </Container>
        </Flex>
    )
}
