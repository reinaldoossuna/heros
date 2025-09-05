import { Checkbox, CheckboxGroup, Checkbox as CkeckboxChakra, Fieldset, SimpleGrid } from '@chakra-ui/react';
import { getLocationsv2ApiLocationV2GetOptions } from "@/client/@tanstack/react-query.gen";
import Separator from '../common/Separator';
import { Location, SensorType } from '@/client';
import { useQuery } from '@tanstack/react-query';
import { ConnectForm } from './connectForm';
import { FieldValues, useController, UseFormReturn } from 'react-hook-form';


const StationSelector = () => {

    const { data: allLocations, status } = useQuery({
        ...getLocationsv2ApiLocationV2GetOptions(),
        staleTime: Infinity,
        placeholderData: []
    });
    if (status === "error") return <></>

    return (

        <ConnectForm>
            {({ watch, control, formState: { errors } }: UseFormReturn<FieldValues, any, FieldValues>) => {
                const dataType = watch("dataType");
                const stationsOptions = allLocations.filter((station) => station.sensor === dataType)

                const stations = useController({
                    control,
                    name: "stations",
                    defaultValue: [],
                });

                const invalid = !!errors.stations;
                return (
                    <>
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
                                        {stationsOptions.map(({ alias }) => (
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
                    </>
                )
            }
            }
        </ ConnectForm>
    )
};

export default StationSelector;
