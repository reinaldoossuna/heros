import { Grid } from '@chakra-ui/react'
import Stats from '../components/common/Stats'

const DashboardLayout = () => (
  <Grid
    templateColumns="repeat(4, 1fr)"
    templateRows="auto 40rem auto"
    gap={'2.4rem'}
  >
    <Stats />
  </Grid>
)

export default DashboardLayout
