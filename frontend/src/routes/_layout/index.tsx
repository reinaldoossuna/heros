import { Box, Heading } from '@chakra-ui/react'
import { createFileRoute } from '@tanstack/react-router'
import {
  MapContainer,
  Marker,
  Popup,
  TileLayer,
  Polyline,
  Tooltip,
  LayersControl,
  LayerGroup,
} from 'react-leaflet'
import { LatLng, LatLngTuple, PointExpression } from 'leaflet'
import { useQuery } from '@tanstack/react-query'
import { getLocationsv2ApiLocationV2GetOptions } from '../../client/@tanstack/react-query.gen.ts'

import L from 'leaflet'
import rulerMarker from '../../assets/ruler.png'
import radarMarker from '../../assets/temperature-sensor.png'
import gaugeMarker from '../../assets/raingauge.png'
import { Location, SensorType } from '../../client/types.gen.ts'

import {
  AnhanduiPolyLine,
  BalsamoPolyLine,
  BandeiraPolyLine,
  CoqueiroPolyLine,
  GameleiraPolyLine,
  GuarirobaPolyLine,
  ImbirussuPolyLine,
  LageadoPolyLine,
  LagoaPolyLine,
  ProsaPolyLine,
  RiberaobotasPolyLine,
  SegredoPolyLine,
} from '@/BaciasShapeFile.ts'
import { Link } from '@tanstack/react-router'
import { SystemHealthStatus } from '../../components/common/SystemHealthStatus'

function get_icon(sensor: SensorType) {
  var url
  var archor: PointExpression = [-0, -0]
  var size: PointExpression = [45, 45]
  if (sensor == SensorType.GAUGE) {
    url = gaugeMarker
  } else if (sensor == SensorType.WEATHER) {
    url = radarMarker
  } else if (sensor == SensorType.LINIGRAFO) {
    url = rulerMarker
    size = [32, 45]
  } else {
    throw 'Not Valid Sensor Type'
  }
  return L.icon({
    iconUrl: url,
    iconRetinaUrl: url,
    popupAnchor: archor,
    iconSize: size,
  })
}

function get_link(location: Location) {
  if (location.sensor === SensorType.GAUGE) {
    return (
      <Link to={'/gauges'} search={{ stations: location.alias }}>
        {' '}
        Veja os dados{' '}
      </Link>
    )
  }
  return <></>
}

export const Route = createFileRoute('/_layout/')({
  component: Dashboard,
})

const shedsToPlot = [
  { positions: ImbirussuPolyLine, name: 'imbirussu', color: 'teal' },
  { positions: CoqueiroPolyLine, name: 'coqueiro', color: 'yellow' },
  { positions: AnhanduiPolyLine, name: 'anhandui', color: 'maroon' },
  { positions: BandeiraPolyLine, name: 'bandeira', color: 'black' },
  { positions: SegredoPolyLine, name: 'segredo', color: 'silver' },
  { positions: BalsamoPolyLine, name: 'balsamo', color: 'purple' },
  { positions: LageadoPolyLine, name: 'lageado', color: 'orange' },
  { positions: LagoaPolyLine, name: 'lagoa', color: 'blue' },
  { positions: GameleiraPolyLine, name: 'gameleira', color: 'green' },
  { positions: RiberaobotasPolyLine, name: 'riberaobotas', color: 'red' },
  { positions: ProsaPolyLine, name: 'prosa', color: 'navy' },
  { positions: GuarirobaPolyLine, name: 'guariroba', color: 'pink' },
]

function Dashboard() {
  const position = new LatLng(-20.4588, -54.6219)

  const { data: allLocations, status } = useQuery({
    ...getLocationsv2ApiLocationV2GetOptions(),
    staleTime: Infinity,
  })

  const sensors_in = (shed: string) => {
    const shed_alias = shed.substring(0, 2)
    return allLocations
      ?.filter((l) => l.sensor === SensorType.GAUGE)
      .map((l) => l.alias)
      .filter((l) => l.toLowerCase().includes(shed_alias))
      .join(',')
  }

  if (status === 'pending') {
    return <span>Loading...</span>
  }
  if (status === 'error' || !Array.isArray(allLocations)) {
    return <span>Error</span>
  }

  return (
    <>
      <Box maxH={'100vh'} pt={12} px={8} py={6}>
        <Heading size={'2xl'} mb={6}>
          Bem-vindo
        </Heading>
        <Box mb={8}>
          <SystemHealthStatus />
        </Box>
        <MapContainer
          style={{ height: '65vh', width: '100%', borderRadius: '8px' }}
          center={position}
          zoom={10}
          scrollWheelZoom={true}
        >
          <LayersControl position="topright">
            <LayersControl.BaseLayer checked name="OpenStreetMap">
              <TileLayer
                maxZoom={13}
                minZoom={11}
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
            </LayersControl.BaseLayer>
            <LayersControl.BaseLayer name="Stamen Toner Lite">
              <TileLayer
                maxZoom={13}
                minZoom={11}
                attribution='&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://tiles.stadiamaps.com/tiles/stamen_toner_lite/{z}/{x}/{y}{r}.png"
              />
            </LayersControl.BaseLayer>
            <LayersControl.BaseLayer name="Esri World Imagery">
              <TileLayer
                maxZoom={13}
                minZoom={11}
                attribution="Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"
                url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
              />
            </LayersControl.BaseLayer>
            <LayersControl.Overlay checked name="Pluviômetros">
              <LayerGroup>
                {allLocations
                  ?.filter((l) => l.sensor === SensorType.GAUGE)
                  .map((d) => (
                    <Marker
                      key={d.alias}
                      position={[d.latitude, d.longitude]}
                      icon={get_icon(d.sensor)}
                    >
                      <Popup>
                        Nome: {d.alias} <br />
                        Status: {d.status} <br />
                        Loc: {[d.latitude.toFixed(4), d.longitude.toFixed(4)]}{' '}
                        <br />
                        {get_link(d)}
                      </Popup>
                    </Marker>
                  ))}
              </LayerGroup>
            </LayersControl.Overlay>
            <LayersControl.Overlay checked name="Metereológicos">
              <LayerGroup>
                {allLocations
                  ?.filter((l) => l.sensor === SensorType.WEATHER)
                  .map((d) => (
                    <Marker
                      key={d.alias}
                      position={[d.latitude, d.longitude]}
                      icon={get_icon(d.sensor)}
                    >
                      <Popup>
                        Nome: {d.alias} <br />
                        Status: {d.status} <br />
                        Loc: {[d.latitude.toFixed(4), d.longitude.toFixed(4)]}{' '}
                        <br />
                        {get_link(d)}
                      </Popup>
                    </Marker>
                  ))}
              </LayerGroup>
            </LayersControl.Overlay>
            <LayersControl.Overlay checked name="Linígrafos">
              <LayerGroup>
                {allLocations
                  ?.filter((l) => l.sensor === SensorType.LINIGRAFO)
                  .map((d) => (
                    <Marker
                      key={d.alias}
                      position={[d.latitude, d.longitude]}
                      icon={get_icon(d.sensor)}
                    >
                      <Popup>
                        Nome: {d.alias} <br />
                        Status: {d.status} <br />
                        Loc: {[d.latitude.toFixed(4), d.longitude.toFixed(4)]}{' '}
                        <br />
                        {get_link(d)}
                      </Popup>
                    </Marker>
                  ))}
              </LayerGroup>
            </LayersControl.Overlay>
            <LayersControl.Overlay checked name="Bacias">
              <LayerGroup>
                {shedsToPlot.map((shed) => (
                  <Polyline
                    key={shed.name}
                    pathOptions={{
                      fill: true,
                      fillOpacity: 0.1,
                      color: shed.color,
                    }}
                    positions={shed.positions as LatLngTuple[]}
                  >
                    <Tooltip sticky>{shed.name}</Tooltip>

                    <Popup>
                      <Link
                        to={'/gauges'}
                        search={{ stations: sensors_in(shed.name) }}
                      >
                        Veja os dados dos Pluviômetros nesta bacia
                      </Link>
                    </Popup>
                  </Polyline>
                ))}
              </LayerGroup>
            </LayersControl.Overlay>
          </LayersControl>
        </MapContainer>
      </Box>
    </>
  )
}
