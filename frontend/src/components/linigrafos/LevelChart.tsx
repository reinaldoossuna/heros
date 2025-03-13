import moment from 'moment';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { formatter_tooltip } from '../../utils'
import { getLocalAvgDataApiLinigrafosAvgLocalIntervalGetOptions } from '../../client/@tanstack/react-query.gen';
import { useQuery } from '@tanstack/react-query';
import { Box, Heading, Skeleton } from '@chakra-ui/react';

const LevelChart = ({ location }: { location: string }) => {
    const { data, status } = useQuery({
        ...getLocalAvgDataApiLinigrafosAvgLocalIntervalGetOptions(
            {
                path: { local: location, interval: 'hourly' },
                query: { daysago: 5 }
            }
        )
    })

    if (status === 'pending') {
        return <span>Loading...</span>
    }

    if (status === 'error' || typeof (data) === undefined) {
        return <span>Error</span>
    }

    return (
        <Box padding={"1rem"}>
            <Heading size={"sm"} marginBottom={"1rem"}>
                {location}
            </Heading>
            {
                data.length == 0 ?
                    <Skeleton height="200px" variant="none" marginX={"40px"} /> :
                    <ResponsiveContainer width="100%" height={200}>
                        <AreaChart
                            width={500}
                            height={200}
                            data={data}
                            syncId="levelId"
                            margin={{
                                top: 10,
                                right: 30,
                                left: 0,
                                bottom: 0,
                            }}
                        >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis
                                name='Data'
                                dataKey={d => d.date.getTime()}
                                domain={[data[0].date.getTime(), data[data.length - 1].date.getTime()]}
                                tickFormatter={(value, _) => moment(value).format('DD/M HH:mm')}
                                scale="time" type="number" />
                            <YAxis />
                            <Tooltip labelFormatter={(value) => moment(value).format('DD/M/Y HH:mm')} formatter={formatter_tooltip} />
                            {/* TODO: Clean data before ploting */}
                            <Area type="monotone" name="Altura" dataKey={d => d.avg_height} stroke="#2257A0" fill="#51AFEF" />
                        </AreaChart>
                    </ResponsiveContainer>
            }
        </Box>
    )
};

export default LevelChart;
