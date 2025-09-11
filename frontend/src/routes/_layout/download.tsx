import { downloadDataApiDownloadPost } from "@/client";
import LayoutBox from "@/components/common/LayoutBox";
import PeriodSelector from "@/components/download/periodSelector";
import StationSelector from "@/components/download/stationSelector";
import { TypeSelect } from '@/components/download/TypeSelect';
import { Button } from "@/components/ui/button";
import { VStack } from "@chakra-ui/react"

import { createFileRoute } from "@tanstack/react-router";
import { FormProvider, useForm } from "react-hook-form";

export const Route = createFileRoute("/_layout/download")({
    component: DownloadComponent,
});

const sendBlob2User = (blob: Blob, filename: string) => {
    // Temp URL for blob
    const url = window.URL.createObjectURL(blob);

    // Temp link and Click
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();

    // Clean up all temps
    link.remove();
    window.URL.revokeObjectURL(url);
}

function DownloadComponent() {

    const methods = useForm()
    const onSubmit = async (v) => {
        const response = await downloadDataApiDownloadPost({
            body: {
                dataType: v.dataType,
                period: {
                    begin: v.period_begin,
                    end: v.period_end
                },
                stations: v.stations
            }
        })
        console.log(response)
        sendBlob2User(response.data, "data.zip")
    }

    return (

        <LayoutBox>
            <LayoutBox.Title>
                Download Data
            </LayoutBox.Title>
            <FormProvider {...methods}>
                <form onSubmit={methods.handleSubmit(onSubmit)}>
                    <VStack alignItems={'flex-start'}>
                        <TypeSelect />
                        <PeriodSelector />
                        <StationSelector />
                        <Button marginY={10} type="submit" >
                            Download
                        </Button>
                    </VStack>
                </form>
            </FormProvider>
        </LayoutBox>
    );
}
