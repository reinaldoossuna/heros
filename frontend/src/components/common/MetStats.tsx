import { IoArrowDown, IoThermometerSharp } from "react-icons/io5";
import { Stat, Status } from "./Stat"
import { GiRaining, GiWaterDrop } from "react-icons/gi";
import { MetereologicoData } from "../../client";

const filter_data = (data: Array<MetereologicoData>, key: keyof MetereologicoData) => {
    /* Make TS happy */
    if (key === 'data') return [];

    const clean = data.map(d => d[key]).filter(v => v !== null)
    return clean
}

const mean = (data: Array<MetereologicoData>, key: keyof MetereologicoData) => {
    const clean = filter_data(data, key)
    const mean = clean.reduce((acc, v) => acc + v) / clean.length
    return mean
}

const MetStats = ({ data }: { data: Array<MetereologicoData> }) => {
    const mean_temp = mean(data, 'temperatura')
    const mean_atm = mean(data, 'pressao_atmosferica')
    const rain_acc = filter_data(data, 'precipitacao').reduce((acc, v) => acc + v)
    const mean_rh = mean(data, 'umidade_ar')

    return (
        <>
            <Stat icon={IoArrowDown} title="Pressao Atmosferica" color={Status.Ok}>{`${mean_atm.toFixed(1)} bar`}</Stat>
            <Stat icon={IoThermometerSharp} title="Temp. Media" color={Status.Ok}>{`${mean_temp.toFixed(1)} °C`}</Stat>
            <Stat icon={GiRaining} title="Chuva Acumulada" color={Status.Ok}>{`${rain_acc.toFixed(1)} mm`}</Stat>
            <Stat icon={GiWaterDrop} title="Umidade do ar" color={Status.Ok}>{`${mean_rh.toFixed(1)} %`}</Stat>
        </>
    )
};

export default MetStats;
