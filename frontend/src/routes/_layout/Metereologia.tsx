import { Grid, GridItem } from "@chakra-ui/react"
import { Box, Heading} from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"
import { getDataApiMetereologicoGetOptions } from '../../client/@tanstack/react-query.gen';

import moment from 'moment';
import { useQuery } from '@tanstack/react-query';
import MetStats from "../../components/common/MetStats"
import Charts from "../../components/metereologia/Charts"


export const Route = createFileRoute("/_layout/Metereologia")({
    component: Dashboard,
})

function Dashboard() {


    const { data, status } = useQuery({
        ...getDataApiMetereologicoGetOptions({
            query: {
                start: moment().utc().subtract(1, 'day').startOf('day').toDate(),
                end: moment().utc().subtract(1, 'day').endOf('day').toDate()
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
                <Heading size={"2xl"}>
                    Metereologia
                </Heading>
                <Grid templateColumns="repeat(5, 1fr)" templateRows="10rem auto" gap={"2.4rem"} height={"auto"}>
                    <MetStats data={data} />
                    <GridItem gridRow={2} colSpan={4}>
                        <Charts data={data} />
                    </GridItem>
                </Grid>
            </Box>
        </>
    )
}
