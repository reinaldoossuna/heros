"use client"

import { SensorType } from "@/client"
import { useStations } from "@/hooks/useStation"
import {
    Badge,
    Combobox,
    Portal,
    Wrap,
    WrapItem,
    createListCollection,
} from "@chakra-ui/react"
import { useMemo, useState } from "react"

export const allnone = "Todos/Nenhum";

const StationSelect = ({ selected, onChange }: { selected: string[]; onChange: (details: any) => void }) => {
    const { stations } = useStations(SensorType.GAUGE);
    const [searchValue, setSearchValue] = useState("")
    const filteredItems = useMemo(
        () => [allnone].concat(stations)
            .filter((item) =>
                item.toLowerCase().includes(searchValue.toLowerCase()),
            ),
        [stations, searchValue],
    )

    const collection = useMemo(
        () => createListCollection({ items: filteredItems }),
        [filteredItems],
    )
    return (
        <Combobox.Root
            multiple
            closeOnSelect
            width="420px"
            value={selected}
            collection={collection}
            onValueChange={onChange}
            onInputValueChange={(details) => setSearchValue(details.inputValue)}
        >
            <Wrap gap="2">
                {selected.map((station) => (
                    <Badge key={station}>{station}</Badge>
                ))}
                {selected.length === 0 &&
                    <WrapItem marginBottom={5}>
                    </WrapItem>
                }
            </Wrap>

            <Combobox.Label>Selectione as Estacoes: </Combobox.Label>

            <Combobox.Control>
                <Combobox.Input />
                <Combobox.IndicatorGroup>
                    <Combobox.Trigger />
                </Combobox.IndicatorGroup>
            </Combobox.Control>

            <Portal>
                <Combobox.Positioner>
                    <Combobox.Content>
                        <Combobox.ItemGroup>
                            {filteredItems.map((item) => (
                                <Combobox.Item key={item} item={item}>
                                    {item}
                                    <Combobox.ItemIndicator />
                                </Combobox.Item>
                            ))}
                            <Combobox.Empty>No station found</Combobox.Empty>
                        </Combobox.ItemGroup>
                    </Combobox.Content>
                </Combobox.Positioner>
            </Portal>
        </Combobox.Root>
    )
}
export default StationSelect;
