import { Field, HStack, Input } from '@chakra-ui/react';
import Separator from '../common/Separator';
import { ConnectForm } from './connectForm';

export class Period {
    from?: Date;
    to?: Date;
}

const PeriodSelector = () => (
    <ConnectForm>
        {
            ({ register }) =>
                <>
                    <Separator label={"Periodo de dados"} />
                    <HStack marginLeft={2}>
                        <Field.Root>
                            <Field.Label>
                                From: <Field.RequiredIndicator />
                            </Field.Label>
                            <Input type="date" width={"320px"} {...register("period_begin", { valueAsDate: true })} />
                        </Field.Root>
                        <Field.Root >
                            <Field.Label>
                                To: <Field.RequiredIndicator />
                            </Field.Label>
                            <Input type="date" width={"320px"} {...register("period_end", { valueAsDate: true })} />
                        </Field.Root>
                    </HStack>
                </>
        }
    </ConnectForm>
);

export default PeriodSelector;
