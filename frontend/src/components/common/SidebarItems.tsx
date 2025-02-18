import { Box, Flex, Icon, Text, useColorModeValue } from "@chakra-ui/react"
import { Link } from "@tanstack/react-router"
import { TiBook, TiDownloadOutline, TiHome, TiWeatherShower } from "react-icons/ti"
import { TbLineHeight, TbReportAnalytics } from "react-icons/tb"

const items = [
    { icon: TiHome, title: "Home", path: "/" },
    { icon: TiWeatherShower, title: "Metereologia", path: "/metereologia" },
    { icon: TbLineHeight, title: "Sensores de nivel", path: "/linigrafos" },
    { icon: TiDownloadOutline, title: "Download", path: "/download" },
    { icon: TbReportAnalytics, title: "Report", path: "/report" },
    { icon: TiBook, title: "About", path: "/about" }
]

export default function SidebarItems() {
    const fgColor = useColorModeValue("ui.dark", "ui.light")

    const listItems = items.map(({ icon, title, path }) => (

        <Flex
            as={Link}
            to={path}
            w="100%"
            p={2}
            key={title}
        >
            <Icon as={icon} alignSelf="center" color={fgColor} />
            <Text ml={2} color={fgColor}> {title}</Text>
        </Flex>
    ))

    return (
        <Box>
            {listItems}
        </Box>
    )

}
