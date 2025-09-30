import { getDailyStationDataApiGaugesDailyStationGetOptions } from '@/client/@tanstack/react-query.gen';
import { Flex, Heading, Spinner } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import moment from 'moment';
import { Bar, CartesianGrid, ComposedChart, Line, Tooltip, XAxis, YAxis } from 'recharts';

interface chartPropTypes {
    location: String,
    year: Number
}

const Chart = ({ station, year }: chartPropTypes) => {

    const { data, error, status } = useQuery({
        ...getDailyStationDataApiGaugesDailyStationGetOptions({
            keepPreviousData: true,
            path: { station: station }, query: { start: new Date(year, 0, 1), end: new Date(year + 1, 0, 1) },

        }),
        retry: false
    })

    const cumulativeSum = (sum => value => {
        sum += value.data
        return { ...value, "acc": sum }
    })(0);


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
                    data={data.map(cumulativeSum)}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis
                        dataKey={d => moment(d.time).dayOfYear()}
                        domain={[moment(`01/01/${year}`).dayOfYear(), moment(`31/12/${year}`).dayOfYear()]}
                        ticks={[...Array(12).keys()].map(i => i + 1).map(m => moment(`${year}/${m}/01`).dayOfYear())}

                        tickFormatter={(value, _) => moment(`01/01/${year}`).dayOfYear(value).format("DD/MM")}
                        scale="time" type="number"
                    />
                    <YAxis yAxisId="discrete" orientation="left" domain={[0, 50]} />
                    <YAxis yAxisId="accumulated" orientation="right" domain={[0, 200]} />

                    <Tooltip labelFormatter={(value) => moment(`01/01/${year}`).dayOfYear(value).format("DD/MM/YYYY")
                width={1000}
                height={250}
                    } />
                    <Bar yAxisId={"discrete"} dataKey="data" fill="#82ca9d" />
                    <Line yAxisId={"accumulated"} type="monotone" dataKey={"acc"} stroke="#ff7300" />

                </ComposedChart>
        }
    </Flex>

};

export { Chart };
