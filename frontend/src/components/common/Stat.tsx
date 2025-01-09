import { Text, Icon, chakra, Heading, useColorModeValue } from "@chakra-ui/react"
import { IconType } from "react-icons"

const Card = chakra('div', {
    baseStyle: {
        display: "grid",
        gridTemplateColumns: "6.4rem 1fr",
        gridTemplateRows: "auto auto",
        p: '1.6rem',
        rounded: 'sm',
        shadow: 'lg',
        bg: "inherit"
    },
}
)

export enum Status {
    Good = "green.100",
    Bad = "red.100",
    Ok = "blue.100"
}

interface StatProps {
    icon: IconType
    color: Status
    title: String
    children: React.ReactNode
}



export function Stat({ icon, color, title, children }: StatProps) {

    const fgColor = useColorModeValue("ui.dark", "ui.light")
    return <Card>
        <Icon as={icon} alignSelf={"center"} color={fgColor} bg={color} rounded={"50%"} width={"5.2rem"} height={"5.2rem"} padding={".5rem"} gridRow={"1/-1"} />
        <Heading size={"md"}>
            {title}
        </Heading>
        <Text textStyle="7xl">
            {children}
        </Text>
    </Card>
}
