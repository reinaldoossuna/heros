import L from 'leaflet'
import { PointExpression } from 'leaflet'

import rulerMarker from '../../assets/ruler.png'
import radarMarker from '../../assets/temperature-sensor.png'
import gaugeMarker from '../../assets/raingauge.png'
import { SensorType } from '../../client/types.gen'

export function get_icon(sensor: SensorType) {
  let url
  const archor: PointExpression = [-0, -0]
  let size: PointExpression = [45, 45]
  if (sensor === SensorType.GAUGE) {
    url = gaugeMarker
  } else if (sensor === SensorType.WEATHER) {
    url = radarMarker
  } else if (sensor === SensorType.LINIGRAFO) {
    url = rulerMarker
    size = [32, 45]
  } else {
    throw new Error('Not Valid Sensor Type')
  }
  return L.icon({
    iconUrl: url,
    iconRetinaUrl: url,
    popupAnchor: archor,
    iconSize: size,
  })
}

