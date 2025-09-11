import { UseFormReturn, FieldValues } from 'react-hook-form';
import { ConnectForm } from './connectForm';
import { createListCollection, Field, NativeSelect } from "@chakra-ui/react";
import { SensorType } from '@/client';

const dataTypes = createListCollection({
    items: [
        { label: "Metereologico", value: SensorType.WEATHER },
        { label: "Sensore de Nivel", value: SensorType.LINIGRAFO },
        { label: "Pluviometros", value: SensorType.GAUGE },
    ],
})

type SelectItem = {
    value: SensorType,
    label: string
}

export const TypeSelect = () => (

    <ConnectForm>
        {({ register, formState: { errors } }: UseFormReturn<FieldValues, any, FieldValues>) => <Field.Root invalid={!!errors.dataType} marginY={2}>
            <Field.Label>
                Sensor
            </Field.Label>
            <NativeSelect.Root size="sm" width="240px">
                <NativeSelect.Field
                    placeholder="Select option"
                    {...register("dataType")}
                >
                    {dataTypes.items.map((type: SelectItem) => (
                        <option key={type.value} value={type.value}>
                            {type.label}
                        </option>
                    ))}

                </NativeSelect.Field>
                <NativeSelect.Indicator />
            </NativeSelect.Root>
            <Field.ErrorText>{errors.dataType?.message as string}</Field.ErrorText>
        </Field.Root>}
    </ConnectForm>
);
