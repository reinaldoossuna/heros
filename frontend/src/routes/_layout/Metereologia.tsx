import { Flex, Grid, GridItem, Input, Text } from "@chakra-ui/react"
import { Box, Heading } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"
import { getDataApiMetereologicoGetOptions } from '../../client/@tanstack/react-query.gen';

import moment from 'moment';
import { useQuery } from '@tanstack/react-query';
import MetStats from "../../components/common/MetStats"
import Charts from "../../components/metereologia/Charts"
import { useState } from "react";


export const Route = createFileRoute("/_layout/Metereologia")({
    component: Dashboard,
})

function Dashboard() {
    const [date, setDate] = useState(moment().utc().subtract(1, 'day'))


    const { data, status } = useQuery({
        ...getDataApiMetereologicoGetOptions({
            query: {
                start: date.startOf('day').toDate(),
                end: date.endOf('day').toDate()
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
                    Meteorologia
                </Heading>

                <Flex marginY={5} align={'end'} justifyContent={'flex-begin'}>
                    <Input
                        max={moment().format("YYYY-MM-DD")}
                        type="date" width={"320px"} value={date.format("YYYY-MM-DD")} onChange={(e) => {
                            setDate(moment(e.target.value))
                        }} />
                </Flex>
                {data.length !== 0 &&
                    < Grid templateColumns="repeat(5, 1fr)" templateRows="10rem auto" gap={"2.4rem"} height={"auto"}>
                        <MetStats data={data} />
                        <GridItem gridRow={2} colSpan={4}>
                            <Charts data={data} />
                        </GridItem>
                    </Grid>
                }
                {data.length === 0 &&
                    <Text>
                        No data for this day
                    </Text>
                }
            </Box >
        </>
    )
}
