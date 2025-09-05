import { Box, Flex, Icon, Text } from "@chakra-ui/react"
import { Link } from "@tanstack/react-router"
import { TiBook, TiDownloadOutline, TiHome, TiWeatherShower } from "react-icons/ti"
import { TbLineHeight, TbReportAnalytics, TbCloudRain } from "react-icons/tb"


const items = [
    { icon: TiHome, title: "Home", path: "/" },
    { icon: TiWeatherShower, title: "Metereologia", path: "/metereologia" },
    { icon: TbLineHeight, title: "Sensores de nivel", path: "/linigrafos" },
    { icon: TbCloudRain, title: "Pluviometros", path: "/gauges" },
    { icon: TiDownloadOutline, title: "Download", path: "/download" },
    { icon: TbReportAnalytics, title: "Report", path: "/report" },
    { icon: TiBook, title: "About", path: "/about" }
]

export default function SidebarItems() {

    const listItems = items.map(({ icon, title, path }) => (

        <Flex
            as={Link}
            to={path}
            w="100%"
            p={2}
            key={title}
        >
            <Icon as={icon} alignSelf="center" />
            <Text ml={2}> {title}</Text>
        </Flex>
    ))

    return (
        <Box>
            {listItems}
        </Box>
    )

}
