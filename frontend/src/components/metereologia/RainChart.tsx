import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { MetereologicoData } from '../../client';
import moment from 'moment';
import { formatter_tooltip } from '../../utils';

const RainChart = ({ data }: { data: Array<MetereologicoData> }) => {

    return (
        <ResponsiveContainer width="100%" height={300}>
            <BarChart
                width={500}
                height={300}
                data={data}
                syncId="metId"
                margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                }}
            >
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis
                    dataKey={d => d.data.getTime()}
                    domain={[data[0].data.getTime(), data[data.length - 1].data.getTime()]}
                    tickFormatter={(value, _) => moment(value).format('HH:mm')}
                    scale="time" type="number" />
                <YAxis />
                <Tooltip labelFormatter={(value) => moment(value).format('d/M/Y HH:mm')} formatter={formatter_tooltip} />
                <Bar name="Precipitacao" dataKey="precipitacao" fill="#2257A0" activeBar={{ r: 8 }} />
            </BarChart>
        </ResponsiveContainer >
    )
};

export default RainChart;
