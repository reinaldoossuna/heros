import L from 'leaflet'
import { PointExpression } from 'leaflet'
import { Link } from '@tanstack/react-router'
import React from 'react'

import rulerMarker from '../../../assets/ruler.png'
import radarMarker from '../../../assets/temperature-sensor.png'
import gaugeMarker from '../../../assets/raingauge.png'
import { Location, SensorType } from '../../../client/types.gen'

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
