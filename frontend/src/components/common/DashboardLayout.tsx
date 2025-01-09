import { Grid, GridItem } from "@chakra-ui/react"
import Stats from "./Stats"
import Chart from "./Chart";

const DashboardLayout = ({}) => (

    <Grid templateColumns="repeat(4, 1fr)" templateRows="10rem auto" gap={"2.4rem"} height={"auto"}>
        <Stats />
        <GridItem gridRow={2} colSpan={3}>
            <Chart />
        </GridItem>
    </Grid>
);

export default DashboardLayout;
