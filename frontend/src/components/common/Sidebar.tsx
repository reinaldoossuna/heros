import { Box, Flex, useColorModeValue, Image, Text } from "@chakra-ui/react";
import HerosLogo from "../../assets/heros.jpg"

import SidebarItems from "./SidebarItems"

export default function Sidebar() {
    const bgColor = useColorModeValue("ui.light", "ui.dark")
    const fgColor = useColorModeValue("ui.dark", "ui.light")
    const secBgColor = useColorModeValue("ui.secondary", "ui.darkSlate")

    return (
        <Box
            bg={bgColor}
            p={3}
            h="100vh"
            position={"sticky"}
            top="0"
            display={"flex"}
        >
            <Flex
                flexDir="column"
                justify={"space-between"}
                bg={secBgColor}
                p={4}
                borderRadius={12}
            >
                <Box>
                    <Image src={HerosLogo} alt="Logo" w="180px" maxW="2xs" p={6} />
                    <SidebarItems />
                </Box>
                <Text color={fgColor}
                    noOfLines={2}
                    fontSize="sm"
                    p={2}
                    maxW="180px"
                >
                    Lorem
                </Text>
            </Flex>
        </Box>
    )
}
