import { Checkbox, CheckboxGroup, Fieldset, SimpleGrid } from '@chakra-ui/react';
import Separator from '../common/Separator';
import { SensorType } from '@/client';
import { ConnectForm } from './connectForm';
import { FieldValues, useController, UseFormReturn } from 'react-hook-form';
import { useStations } from '@/hooks/useStation';


const StationSelector = () => {

    return (

        <ConnectForm>
            {({ watch, control, formState: { errors } }: UseFormReturn<FieldValues, any, FieldValues>) => {
                const dataType = watch("dataType");
                const { stations: stationsOptions } = useStations(dataType)

                const stations = useController({
                    control,
                    name: "stations",
                    defaultValue: [],
                });
                console.log(stationsOptions)

                const invalid = !!errors.stations;
                return (
                    <>
                        {dataType !== SensorType.WEATHER &&
                            dataType !== "" &&
                            dataType !== undefined &&
                            <Fieldset.Root invalid={invalid}>
                                <Fieldset.Legend>
                                    <Separator label={"Selecione estacoes"} />
                                </Fieldset.Legend>
                                <CheckboxGroup
                                    invalid={invalid}
                                    value={stations.field.value}
                                    onValueChange={stations.field.onChange}
                                    name={stations.field.name}
                                >
                                    <Fieldset.Content>
                                        <SimpleGrid columns={5} columnGap="5" rowGap="6">
                                            {stationsOptions.map(alias => (
                                                <Checkbox.Root key={alias} value={alias} size={"sm"}>
                                                    <Checkbox.HiddenInput />
                                                    <Checkbox.Control />
                                                    <Checkbox.Label>{alias}</Checkbox.Label>
                                                </Checkbox.Root>
                                            ))}
                                        </SimpleGrid>
                                    </Fieldset.Content>
                                </CheckboxGroup>
                            </Fieldset.Root>
                        }
                    </>
                )
            }
            }
        </ ConnectForm>
    )
};

export default StationSelector;
