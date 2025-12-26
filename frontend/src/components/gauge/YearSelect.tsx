import { range } from '@/utils'
import moment from 'moment'
import { Portal, Select, createListCollection } from '@chakra-ui/react'

const minYear = 2016
const maxYear = moment({}).year()
const years = createListCollection({
  items: range(maxYear - minYear + 1, minYear).map((y) => y.toString()),
})

const YearSelect = ({
  year,
  onChange,
}: {
  year: string
  onChange: (details: any) => void
}) => {
  return (
    <Select.Root collection={years} width="120px" onValueChange={onChange}>
      <Select.HiddenSelect />
      <Select.Label>Ano: </Select.Label>
      <Select.Control>
        <Select.Trigger>
          <Select.ValueText placeholder={year} />
        </Select.Trigger>
        <Select.IndicatorGroup>
          <Select.Indicator />
        </Select.IndicatorGroup>
      </Select.Control>
      <Portal>
        <Select.Positioner>
          <Select.Content>
            {years.items.map((year) => (
              <Select.Item item={year} key={year}>
                {year}
                <Select.ItemIndicator />
              </Select.Item>
            ))}
          </Select.Content>
        </Select.Positioner>
      </Portal>
    </Select.Root>
  )
}

export default YearSelect
