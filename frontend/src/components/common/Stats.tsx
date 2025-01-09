import { IoHardwareChipSharp, IoReloadCircleSharp } from "react-icons/io5";
import { Stat, Status } from "./Stat"
import { MdCastConnected } from "react-icons/md";
const Stats = ({}) => (
    <>
        <Stat icon={IoHardwareChipSharp} title="Sensors" color={Status.Good}> 5/5</Stat>
        <Stat icon={IoReloadCircleSharp} title="Last Update" color={Status.Good}>05/01/2025</Stat>
        <Stat icon={MdCastConnected} title="Status APIs" color={Status.Ok}>Ok</Stat>
    </>
);

export default Stats;
