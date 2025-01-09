import TemperatureChart from './TemperatureChart';
import RainChart from './RainChart';
import { MetereologicoData } from '../../client';



const Charts = ({ data }: { data: Array<MetereologicoData> }) => {
    return (
        <>
            <TemperatureChart data={data} />
            <RainChart data={data} />
        </>
    );

}
export default Charts;
