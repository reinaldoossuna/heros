import { Combobox, Flex, Select } from "@chakra-ui/react"
import { Box, Heading } from "@chakra-ui/react"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import moment from "moment";
import { useMemo, useState } from "react";
import { Chart } from "@/components/gauge/Chart";
import StationSelect from "@/components/gauge/StationSelect";
import YearSelect from "@/components/gauge/YearSelect";
import { SensorType } from "@/client";
import { useStations } from "@/hooks/useStation";

type GaugeSearch = {
    year: number
    stations: string[]
}

export const Route = createFileRoute("/_layout/gauges")({
    component: Dashboard,
    validateSearch: (search: Record<string, unknown>): GaugeSearch => {
        return {
            year: Number(search?.year ?? moment({}).year()),
            stations: search.stations?.split(',') ?? [],
        }
    },
})

function Dashboard() {
    const { year: path_year, stations: path_stations } = Route.useSearch()
    const navigate = useNavigate()
    const { stations } = useStations(SensorType.GAUGE);
    const [year, setYear] = useState(path_year)
    const [selectedStations, setSelectedStations] = useState<string[]>(path_stations)
    console.log(path_stations)


    useMemo(() => {
        setSelectedStations(old => old.length === 0 ? stations : old)
    }, [stations])

    const handleStationsChange = (details: Combobox.ValueChangeDetails) => {
        if (details.value.find((v) => v === 'none')) {
            setSelectedStations([])

            navigate({ search: prev => ({ year: prev.year }) })
            return;
        }
        setSelectedStations(details.value)
        navigate({ search: prev => ({ ...prev, stations: details.value.join(','), }) })
    }

    const handleYearChange = (details: Select.ValueChangeDetails) => {
        setYear(Number(details.value))
        navigate({ search: prev => ({ year: Number(details.value), stations: prev.stations.join(',') }) })
    }

    return (
        <>
            <Box maxH={"100vh"} pt={12} m={4}>
                <Heading size={"2xl"} margin={"2rem"}>
                    Pluviometros
                </Heading>
                <Flex gap={"2.4rem"} height={"auto"} direction={"column"} alignContent={'center'}>
                    <Flex justifyContent={'flex-end'} align={'end'} gap={5}>
                        <YearSelect year={year} onChange={handleYearChange} /> <StationSelect selected={selectedStations} onChange={handleStationsChange} />
                    </Flex>

                    {selectedStations.map(station =>
                        <Chart key={station} station={station} year={year} />
                    )}

                </Flex>
            </Box>
        </>
    )
}
