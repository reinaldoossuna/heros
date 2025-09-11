import { Box, Heading, } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"
import { MapContainer, Marker, Popup, TileLayer, Polyline, Tooltip } from 'react-leaflet'
import { LatLng, PointExpression } from "leaflet"
import { useQuery } from "@tanstack/react-query"
import { getLocationsv2ApiLocationV2GetOptions } from "../../client/@tanstack/react-query.gen.ts"

import L from 'leaflet';
import rulerMarker from '../../assets/ruler.png'
import radarMarker from '../../assets/temperature-sensor.png'
import gaugeMarker from '../../assets/raingauge.png'
import { SensorType } from "../../client/types.gen.ts"

import { AnhanduiPolyLine, BalsamoPolyLine, BandeiraPolyLine, CoqueiroPolyLine, GameleiraPolyLine, GuarirobaPolyLine, ImbirussuPolyLine, LageadoPolyLine, LagoaPolyLine, ProsaPolyLine, RiberaobotasPolyLine, SegredoPolyLine } from "@/BaciasShapeFile.ts"

function get_icon(sensor: SensorType) {
    var url;
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
        throw "Not Valid Sensor Type"
    }
    return L.icon({ iconUrl: url, iconRetinaUrl: url, popupAnchor: archor, iconSize: size })
}


export const Route = createFileRoute("/_layout/")({
    component: Dashboard,
})


const shedsToPlot = [
    { positions: ImbirussuPolyLine, name: 'imbirussu', color: 'teal' },
    { positions: CoqueiroPolyLine, name: 'coqueiro', color: 'yellow' },
    { positions: AnhanduiPolyLine, name: 'anhandui', color: 'maroon' }, { positions: BandeiraPolyLine, name: 'bandeira', color: 'black' },
    { positions: SegredoPolyLine, name: 'segredo', color: 'silver' }, { positions: BalsamoPolyLine, name: 'balsamo', color: 'purple' },
    { positions: LageadoPolyLine, name: 'lageado', color: 'orange' }, { positions: LagoaPolyLine, name: 'lagoa', color: 'blue' },
    { positions: GameleiraPolyLine, name: 'gameleira', color: 'green' }, { positions: RiberaobotasPolyLine, name: 'riberaobotas', color: 'red' },
    { positions: ProsaPolyLine, name: 'prosa', color: 'navy' }, { positions: GuarirobaPolyLine, name: 'guariroba', color: 'pink' }
]

function Dashboard() {

    const position = new LatLng(-20.4588, -54.6219)

    const { data: allLocations, status } = useQuery({
        ...getLocationsv2ApiLocationV2GetOptions(),
        staleTime: Infinity
    });
    if (status === 'pending') {
        return <span>Loading...</span>
    }
    if (status === 'error' || typeof (allLocations) === undefined) {
        return <span>Error</span>
    }

    return (
        <>
            <Box maxH={"100vh"} pt={12} m={4}>
                <Heading size={"4xl"} p={5}>
                    Mapa
                </Heading>
                <MapContainer
                    style={{ height: "70vh", width: "auto" }}
                    center={position} zoom={10} scrollWheelZoom={true}>
                    <TileLayer
                        maxZoom={13}
                        minZoom={11}
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />

                    {allLocations?.map(d => (
                        <Marker key={d.alias} position={[d.latitude, d.longitude]} icon={get_icon(d.sensor)}>
                            <Popup>
                                Nome: {d.alias} <br />
                                Status: {d.status} <br />
                                Loc: {[d.latitude.toFixed(4), d.longitude.toFixed(4)]} <br />
                            </Popup>
                        </Marker>)
                    )}
                    {shedsToPlot.map(shed => <Polyline pathOptions={{ fill: true, fillOpacity: 0.1, color: shed.color }} positions={shed.positions} >
                        <Tooltip sticky>
                            {shed.name}
                        </Tooltip>
                    </Polyline>)}
                </MapContainer>
            </Box>
        </>
    )
}
