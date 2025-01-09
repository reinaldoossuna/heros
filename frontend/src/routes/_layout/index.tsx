import { Box, Heading, useColorModeValue } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet'
import { LatLng } from "leaflet"
import { useQuery } from "@tanstack/react-query"
import { getLocationsApiLocationGetOptions } from "../../client/@tanstack/react-query.gen.ts"

import L from 'leaflet';
import rulerMarker from '../../assets/ruler.png'
import radarMarker from '../../assets/temperature-sensor.png'

const rulerIcon = L.icon({
    iconUrl: rulerMarker,
    iconRetinaUrl: rulerMarker,
    popupAnchor: [-0, -0],
    iconSize: [32, 45]
})

const radarIcon = L.icon({
    iconUrl: radarMarker,
    iconRetinaUrl: radarMarker,
    popupAnchor: [-0, -0],
    iconSize: [45, 45]
})


export const Route = createFileRoute("/_layout/")({
    component: Dashboard,
})


function Dashboard() {

    const fgColor = useColorModeValue("ui.dark", "ui.light")

    const position = new LatLng(-20.4588, -54.6219)
    const wxt_loc = new LatLng(-20.45040, -54.56675)

    const { data, status } = useQuery({
        ...getLocationsApiLocationGetOptions(),
        staleTime: Infinity
    }

    )

    if (status === 'pending') {
        return <span>Loading...</span>
    }
    if (status === 'error' || typeof (data) === undefined) {
        return <span>Error</span>
    }

    return (
        <>
            <Box maxH={"100vh"} pt={12} m={4}>
                <Heading size={"2xl"} color={fgColor} p={5}>
                    Mapa
                </Heading>
                <MapContainer
                    style={{ height: "70vh", width: "auto" }}
                    center={position} zoom={14} scrollWheelZoom={false}>
                    <TileLayer
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />
                    {data.map(d => (
                        <Marker position={[d.latitude, d.longitude]} icon={rulerIcon}>
                            <Popup>
                                {d.nome}
                            </Popup>
                        </Marker>)
                    )}

                    <Marker position={wxt_loc} icon={radarIcon}>
                        <Popup>
                            Localizacao do sensor WXT53
                        </Popup>
                    </Marker>
                </MapContainer>,
            </Box>
        </>
    )
}
