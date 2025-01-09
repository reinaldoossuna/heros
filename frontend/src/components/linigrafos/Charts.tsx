import { SensorDataDB } from '../../client';
import LevelChart from './LevelChart';


const Chart = ({ data }: { data: Array<SensorDataDB> }) => {
    const grouped = Map.groupBy(data, d => d.mac);

    return (
        <div style={{ width: '100vh' }}>

            {
                grouped.values().map((data) => <LevelChart data={data} />)
            }


        </div>
    )
};

export default Chart;
