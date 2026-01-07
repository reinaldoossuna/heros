
import {
  LayersControl,
  LayerGroup,
  Marker,
  Popup,
  TileLayer,
  Polyline,
  Tooltip,
} from 'react-leaflet'
import { LatLngTuple } from 'leaflet'
import { Link } from '@tanstack/react-router'
import { Location, SensorType } from '../../client/types.gen'
import { get_icon } from './mapUtils'
import { shedsToPlot } from './shedsData'

interface MapLayersProps {
  allLocations: Location[]
  sensorsIn: (shed: string) => string
}

interface BaseLayerConfig {
  name: string
  url: string
  attribution: string
  checked?: boolean
}

interface SensorOverlayConfig {
  name: string
  sensorType: SensorType
  checked?: boolean
}

const BASE_LAYER_CONFIGS: BaseLayerConfig[] = [
  {
    name: 'OpenStreetMap',
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    checked: true,
  },
  {
    name: 'Stamen Toner Lite',
    url: 'https://tiles.stadiamaps.com/tiles/stamen_toner_lite/{z}/{x}/{y}{r}.png',
    attribution: '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  },
  {
    name: 'Esri World Imagery',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
  },
]

const SENSOR_OVERLAYS: SensorOverlayConfig[] = [
  { name: 'Pluviômetros', sensorType: SensorType.GAUGE, checked: true },
  { name: 'Metereológicos', sensorType: SensorType.WEATHER, checked: true },
  { name: 'Linígrafos', sensorType: SensorType.LINIGRAFO, checked: true },
]

const MAP_ZOOM_BOUNDS = { minZoom: 11, maxZoom: 13 }

// TODO: This could be improved to handle all sensor types
export function get_link(location: Location) {
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

interface SensorMarkerOverlayProps {
  config: SensorOverlayConfig
  locations: Location[]
}

function SensorMarkerOverlay({ config, locations }: SensorMarkerOverlayProps) {
  const filteredLocations = locations.filter((l) => l.sensor === config.sensorType)

  return (
    <LayersControl.Overlay checked={config.checked} name={config.name}>
      <LayerGroup>
        {filteredLocations.map((location) => (
          <Marker
            key={location.alias}
            position={[location.latitude, location.longitude]}
            icon={get_icon(location.sensor)}
          >
            <Popup>
              Nome: {location.alias} <br />
              Status: {location.status} <br />
              Loc: {[location.latitude.toFixed(4), location.longitude.toFixed(4)]} <br />
              {get_link(location)}
            </Popup>
          </Marker>
        ))}
      </LayerGroup>
    </LayersControl.Overlay>
  )
}

export function MapLayers({ allLocations, sensorsIn }: MapLayersProps) {
  return (
    <LayersControl position="topright">
      {BASE_LAYER_CONFIGS.map((config) => (
        <LayersControl.BaseLayer key={config.name} checked={config.checked} name={config.name}>
          <TileLayer
            {...MAP_ZOOM_BOUNDS}
            attribution={config.attribution}
            url={config.url}
          />
        </LayersControl.BaseLayer>
      ))}
      {SENSOR_OVERLAYS.map((config) => (
        <SensorMarkerOverlay key={config.name} config={config} locations={allLocations} />
      ))}
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
                  search={{ stations: sensorsIn(shed.name) }}
                >
                  Veja os dados dos Pluviômetros nesta bacia
                </Link>
              </Popup>
            </Polyline>
          ))}
        </LayerGroup>
      </LayersControl.Overlay>
    </LayersControl>
  )
}
