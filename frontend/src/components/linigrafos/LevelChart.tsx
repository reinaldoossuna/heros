import moment from 'moment';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { SensorDataDB } from '../../client';
import { formatter_tooltip} from '../../utils'

const LevelChart = ({ data }: { data: Array<SensorDataDB> }) => (

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
                dataKey={d => d.data_leitura.getTime()}
                domain={[data[0].data_leitura.getTime(), data[data.length - 1].data_leitura.getTime()]}
                tickFormatter={(value, _) => moment(value).format('HH:mm')}
                scale="time" type="number" />
            <YAxis />
            <Tooltip labelFormatter={(value) => moment(value).format('DD/M/Y HH:mm')} formatter={formatter_tooltip} />
            {/* TODO: Clean data before ploting */}
            <Area type="monotone" name="Altura" dataKey={d => d.valor_leitura} stroke="#2257A0" fill="#51AFEF" />
        </AreaChart>
    </ResponsiveContainer>
);

export default LevelChart;
