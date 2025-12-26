import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { MetereologicoData } from '../../client'
import moment from 'moment'
import { formatter_tooltip, heat_index } from '../../utils'
import { Box, Text } from '@chakra-ui/react'

const TemperatureChart = ({ data }: { data: Array<MetereologicoData> }) => {
  if (!data || data.length === 0) {
    return (
      <Box p={4} textAlign="center">
        <Text>No temperature data available for this date</Text>
      </Box>
    )
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart
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
          name="Data"
          dataKey={(d) => d.data.getTime()}
          domain={[
            data[0].data.getTime(),
            data[data.length - 1].data.getTime(),
          ]}
          tickFormatter={(value, _) => moment(value).format('HH:mm')}
          scale="time"
          type="number"
        />
        <YAxis />
        <Tooltip
          labelFormatter={(value) => moment(value).format('DD/MM/Y HH:mm')}
          formatter={formatter_tooltip}
        />
        <CartesianGrid stroke="#ccc" />
        <Line
          type="monotone"
          name="Temperatura do ar"
          dataKey="temperatura"
          stroke="#8884d8"
          dot={false}
          activeDot={{ r: 6 }}
        />
        <Line
          type="monotone"
          name="Umidade relativa do ar"
          dataKey="umidade_ar"
          stroke="#51AFEF"
          activeDot={{ r: 6 }}
        />
        <Line
          type="monotone"
          name="Indice de calor"
          dot={false}
          dataKey={(d) => heat_index(d.temperatura, d.umidade_ar)}
          stroke="#DA8548"
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}

export default TemperatureChart
