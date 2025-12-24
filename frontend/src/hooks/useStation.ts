import { SensorType } from "@/client";
import { getLocationsv2ApiLocationV2GetOptions } from "@/client/@tanstack/react-query.gen";
import { useQuery } from "@tanstack/react-query";
import { useMemo } from "react";

const useStations = (type: SensorType) => {

  const { data: allLocations, status } = useQuery({
    ...getLocationsv2ApiLocationV2GetOptions(),
    staleTime: Infinity,
    placeholderData: []
  });

  const stations = useMemo(
    () => ({
      stations: (allLocations ?? [])
        .filter((station) => station.sensor === type)
        .map(station => station.alias)
        .sort((a, b) => a.localeCompare(b)),
      status: status
    }
    ), [allLocations, status, type]
  )

  return stations;

}

export { useStations }
