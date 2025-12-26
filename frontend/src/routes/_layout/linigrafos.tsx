import { Flex } from "@chakra-ui/react"
import { Box, Heading } from "@chakra-ui/react"
import { useQuery } from '@tanstack/react-query';
import { createFileRoute } from "@tanstack/react-router"

import { getLocationsApiLocationGetOptions } from "../../client/@tanstack/react-query.gen"
import LevelChart from "../../components/linigrafos/LevelChart";


export const Route = createFileRoute("/_layout/linigrafos")({
    component: Dashboard,
})

function Dashboard() {


    const { data: locations, status } = useQuery({
        ...getLocationsApiLocationGetOptions({})
    })
    if (status === 'pending') {
        return <span>Loading...</span>
    }
    if (status === 'error' || typeof (locations) === undefined) {
        return <span>Error</span>
    }

    return (
        <>
            <Box maxH={"100vh"} pt={12} m={4}>
                <Heading size={"2xl"} margin={"2rem"}>
                    Sensores de nível - Últimos 5 dias
                </Heading>
                <Flex gap={"2.4rem"} height={"auto"} direction={"column"}>
                    {locations.map(location => <LevelChart location={location.nome} />)}
                </Flex>
            </Box>
        </>
    )
}
