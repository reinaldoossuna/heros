import { GaugeData } from '@/client';
import { getDailyStationDataApiGaugesDailyStationGetOptions } from '@/client/@tanstack/react-query.gen';
import { Flex, Heading, Spinner } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import moment from 'moment';
import { Bar, CartesianGrid, ComposedChart, Line, Tooltip, XAxis, YAxis } from 'recharts';

interface chartPropTypes {
    station: string,
    year: number
}
const format_name = (name: string) => {
    switch (name) {
        case "data": return "Chuva Diária"
        case "acc": return "Chuva Acumulada"
        default: return ""
    }
}

const tooltipFormatter = (value: number, name: string, _props: any) => {
    return [value.toFixed(2), format_name(name)]
};

const Chart = ({ station, year }: chartPropTypes) => {
    if (station === '') {
        return <></>
    }
    const { data, error, status } = useQuery({
        ...getDailyStationDataApiGaugesDailyStationGetOptions({
            // @ts-ignore
            keepPreviousData: true,
            path: { station: station }, query: { start: new Date(year, 0, 1), end: new Date(year + 1, 0, 1) },
        }),
        retry: false
    })

    const cumulativeSum = (sum => (value: GaugeData) => {
        sum += value.data ? value.data : 0
        return { ...value, "acc": sum }
    })(0);

    const d = data?.
        map(cumulativeSum).
        filter((row: GaugeData) => row.time.getFullYear() == year). // making sure the data its from the year we want
        sort((a, b) => a.time.getTime() - b.time.getTime())

    return <Flex gap={"2.4rem"} height={"auto"} direction={"column"} alignContent={'center'}>

        <Heading size={"sm"} marginBottom={"1rem"}>
            {station}

            {status === 'error' &&
                <>
                    {error.name}
                </>
            }

            {status === 'pending' &&
                <Spinner color="teal.500" size="lg" />
            }

            {status === 'success' && data.length === 0 &&
                <>
                    &nbsp;não possui dados no ano {year}.
                </>
            }

        </Heading>
        {status === 'success' && data.length > 0 &&
            <ComposedChart
                data={d}
                margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                }}
                width={1000}
                height={250}
            >
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis
                    dataKey={d => moment(d.time).dayOfYear()}
                    domain={[moment(`01/01/${year}`).dayOfYear(), moment(`31/12/${year}`).dayOfYear()]}
                    ticks={[...Array(12).keys()].map(i => i + 1).map(m => moment(`${year}/${m}/01`).dayOfYear())}

                    tickFormatter={(value, _) => moment(`01/01/${year}`).dayOfYear(value).format("MMM")}
                    scale="time" type="number"
                />
                <YAxis yAxisId="discrete" orientation="left" domain={[0, 50]} unit={'mm'} />
                <YAxis yAxisId="accumulated" orientation="right" domain={[0, 200]} unit={'mm'} />

                <Tooltip
                    formatter={tooltipFormatter}
                    labelFormatter={(value) => moment(`01/01/${year}`).dayOfYear(value).format("DD/MM/YYYY")
                    } />
                <Line yAxisId={"accumulated"} type="monotone" dataKey={"acc"} stroke="#ff7300" dot={false} />
                <Bar yAxisId={"discrete"} dataKey="data" fill="#82ca9d" barSize={5} />
            </ComposedChart>
        }
    </Flex>

};

export { Chart };
