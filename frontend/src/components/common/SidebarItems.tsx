import { Box, Flex, Icon, Text } from "@chakra-ui/react"
import { Link } from "@tanstack/react-router"
import { TiBook, TiDownloadOutline, TiHome, TiWeatherShower } from "react-icons/ti"
import { TbLineHeight, TbCloudRain, TbLock } from "react-icons/tb"


const items = [
    { icon: TiHome, title: "Home", path: "/" },
    { icon: TiWeatherShower, title: "Meteorologia", path: "/metereologia" },
    { icon: TbLineHeight, title: "Sensores de nível", path: "/linigrafos" },
    { icon: TbCloudRain, title: "Pluviômetros", path: "/gauges" },
    { icon: TiDownloadOutline, title: "Download", path: "/download" },
    { icon: TbLock, title: "Credentials", path: "/credentials" },
    { icon: TiBook, title: "About", path: "/about" }
]

export default function SidebarItems() {

    const listItems = items.map(({ icon, title, path }) => (

        <Flex
            asChild
            w="100%"
            p={2}
            key={title}
        >
            <Link to={path}>
            <Icon as={icon} alignSelf="center" />
            <Text ml={2}> {title}</Text>
        </Link>
        </Flex>
    ))

    return (
        <Box>
            {listItems}
        </Box>
    )

}
