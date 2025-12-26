import {
  Flex,
  Grid,
  GridItem,
  Text,
  Box,
  Heading,
  Input,
} from '@chakra-ui/react'
import { createFileRoute } from '@tanstack/react-router'
import {
  getDataApiMetereologicoGetOptions,
  getDataDaysApiMetereologicoDaysGetOptions,
} from '../../client/@tanstack/react-query.gen'

import moment from 'moment'
import { useQuery } from '@tanstack/react-query'
import MetStats from '../../components/common/MetStats'
import Charts from '../../components/metereologia/Charts'
import { useState, useMemo } from 'react'
import { DayPicker } from 'react-day-picker'
import 'react-day-picker/dist/style.css'
import {
  PopoverRoot,
  PopoverTrigger,
  PopoverContent,
} from '../../components/ui/popover'

export const Route = createFileRoute('/_layout/Metereologia')({
  component: Dashboard,
})

function Dashboard() {
  const [date, setDate] = useState(moment().utc().subtract(1, 'day').toDate())

  const { data: availableDays } = useQuery({
    ...getDataDaysApiMetereologicoDaysGetOptions({}),
  })

  const { data, status } = useQuery({
    ...getDataApiMetereologicoGetOptions({
      query: {
        start: moment(date).startOf('day').toDate(),
        end: moment(date).endOf('day').toDate(),
      },
    }),
  })

  const daysWithData = useMemo(() => {
    if (!availableDays) return new Set<string>()
    return new Set(availableDays.map((day) => moment(day).format('YYYY-MM-DD')))
  }, [availableDays])

  const modifiers = useMemo(
    () => ({
      withData: (day: Date) => {
        const dayStr = moment(day).format('YYYY-MM-DD')
        return daysWithData.has(dayStr)
      },
    }),
    [daysWithData]
  )

  const modifiersStyles = {
    withData: {
      backgroundColor: '#c6f6d5',
      color: '#276749',
      fontWeight: 'bold',
    },
  }

  if (status === 'pending') {
    return <span>Loading...</span>
  }
  if (status === 'error' || !Array.isArray(data)) {
    return <span>Error</span>
  }

  return (
    <>
      <Box maxH={'100vh'} pt={12} m={4}>
        <Heading size={'2xl'}>Meteorologia</Heading>

        <Flex marginY={5} align={'start'} justifyContent={'flex-begin'} gap={6}>
          <PopoverRoot>
            <PopoverTrigger asChild>
              <Input
                readOnly
                type="text"
                width={'320px'}
                value={moment(date).format('YYYY-MM-DD')}
                placeholder="Select a date"
                cursor="pointer"
              />
            </PopoverTrigger>
            <PopoverContent>
              <DayPicker
                mode="single"
                selected={date}
                onSelect={(day) => day && setDate(day)}
                disabled={{ after: new Date() }}
                modifiers={modifiers}
                modifiersStyles={modifiersStyles}
              />
            </PopoverContent>
          </PopoverRoot>
          <Box fontSize="sm" mt={2}>
            <Text color="green.600">■ Days with data</Text>
          </Box>
        </Flex>
        {data.length !== 0 && (
          <Grid
            templateColumns="repeat(5, 1fr)"
            templateRows="10rem auto"
            gap={'2.4rem'}
            height={'auto'}
          >
            <MetStats data={data} />
            <GridItem gridRow={2} colSpan={4}>
              <Charts data={data} />
            </GridItem>
          </Grid>
        )}
        {data.length === 0 && <Text>No data for this day</Text>}
      </Box>
    </>
  )
}
