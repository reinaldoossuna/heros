import { Box, Heading } from '@chakra-ui/react'
import { createFileRoute } from '@tanstack/react-router'
import { MapContainer } from 'react-leaflet'
import { LatLng } from 'leaflet'
import { useQuery } from '@tanstack/react-query'
import { getLocationsv2ApiLocationV2GetOptions } from '../../client/@tanstack/react-query.gen.ts'
import { SensorType } from '../../client/types.gen.ts'
import { SystemHealthStatus } from '../../components/common/SystemHealthStatus'
import { MapLayers } from '../../components/map/MapLayers'

export const Route = createFileRoute('/_layout/')({
  component: Dashboard,
})

const DEFAULT_MAP_CENTER = new LatLng(-20.4588, -54.6219)
const DEFAULT_MAP_ZOOM = 10

function Dashboard() {
  const { data: allLocations, status } = useQuery({
    ...getLocationsv2ApiLocationV2GetOptions(),
    staleTime: Infinity,
  })

  const getSensorsIn = (shed: string) => {
    const shedAlias = shed.substring(0, 2)
    return allLocations
      ?.filter((l) => l.sensor === SensorType.GAUGE)
      .map((l) => l.alias)
      .filter((l) => l.toLowerCase().includes(shedAlias))
      .join(',')
  }

  if (status === 'pending') {
    return <span>Loading...</span>
  }
  if (status === 'error' || !Array.isArray(allLocations)) {
    return <span>Error</span>
  }

  return (
    <Box minH={'100vh'} pt={12} px={8} py={6}>
      <Heading size={'2xl'} mb={6}>
        Bem-vindo
      </Heading>
      <Box mb={8}>
        <SystemHealthStatus />
      </Box>
      <MapContainer
        style={{ height: '65vh', width: '100%', borderRadius: '8px' }}
        center={DEFAULT_MAP_CENTER}
        zoom={DEFAULT_MAP_ZOOM}
        scrollWheelZoom
      >
        <MapLayers allLocations={allLocations} sensorsIn={getSensorsIn} />
      </MapContainer>
    </Box>
  )
}
