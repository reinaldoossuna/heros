import { Container, Flex} from "@chakra-ui/react";
import { Outlet, createFileRoute } from "@tanstack/react-router";
import Sidebar from "../components/common/Sidebar"

export const Route = createFileRoute("/_layout")({
    component: Layout,
})

function Layout() {

    return (
        <Flex h="100vh" position="relative">
            <Sidebar />
            <Container maxW="full" overflow={"scroll"}>
                <Outlet />
            </Container>
        </Flex>
    )
}
