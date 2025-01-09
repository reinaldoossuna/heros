import { Grid, GridItem } from "@chakra-ui/react"
import { Box, Heading, useColorModeValue } from "@chakra-ui/react"
import { useQuery } from '@tanstack/react-query';
import { createFileRoute } from "@tanstack/react-router"
import moment from 'moment';

import Charts from "../../components/linigrafos/Charts"
import { getDataApiLinigrafosGetOptions } from "../../client/@tanstack/react-query.gen"


export const Route = createFileRoute("/_layout/linigrafos")({
    component: Dashboard,
})

function Dashboard() {

    const fgColor = useColorModeValue("ui.dark", "ui.light")

    const { data, status } = useQuery({
        ...getDataApiLinigrafosGetOptions({
            query: {
                start: moment().utc().subtract(1, 'day').startOf('day').toDate(),
                end: moment().subtract(1, 'day').endOf('day').toDate()
            },

        }),
    })
    if (status === 'pending') {
        return <span>Loading...</span>
    }
    if (status === 'error' || typeof (data) === undefined) {
        return <span>Error</span>
    }

    return (
        <>
            <Box maxH={"100vh"} pt={12} m={4}>
                <Heading size={"2xl"} color={fgColor}>
                    Sensores de nivel
                </Heading>
                <Grid templateColumns="repeat(5, 1fr)" templateRows="10rem auto" gap={"2.4rem"} height={"auto"}>
                    {/* <MetStats /> */}
                    <GridItem gridRow={2} colSpan={4}>
                        <Charts data={data} />
                    </GridItem>
                </Grid>
            </Box>
        </>
    )
}
