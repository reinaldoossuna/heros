import { Box, Heading, Grid } from '@chakra-ui/react'
import { useQuery } from '@tanstack/react-query'
import { healthCheckApiHealthGetOptions } from '../../client/@tanstack/react-query.gen.ts'
import { Stat, Status } from './Stat'
import {
  FaDatabase,
  FaCloud,
  FaServer,
  FaCheckCircle,
  FaExclamationTriangle,
  FaTimesCircle,
  FaQuestion,
} from 'react-icons/fa'
import { IconType } from 'react-icons'

function getStatusColor(
  status: 'healthy' | 'degraded' | 'unhealthy' | 'unknown'
): Status {
  switch (status) {
    case 'healthy':
      return Status.Good
    case 'degraded':
      return Status.Ok
    case 'unhealthy':
      return Status.Bad
    case 'unknown':
      return Status.Unknown
  }
}

function getStatusIcon(
  status: 'healthy' | 'degraded' | 'unhealthy' | 'unknown'
): IconType {
  switch (status) {
    case 'healthy':
      return FaCheckCircle
    case 'degraded':
      return FaExclamationTriangle
    case 'unhealthy':
      return FaTimesCircle
    case 'unknown':
      return FaQuestion
  }
}

function getServiceIcon(serviceName: string): IconType {
  const lowerName = serviceName.toLowerCase()
  if (lowerName.includes('noaa')) return FaCloud
  if (lowerName.includes('engtec')) return FaServer
  return FaServer
}

export function SystemHealthStatus() {
  const { data: healthData } = useQuery({
    ...healthCheckApiHealthGetOptions(),
    refetchInterval: 30000,
  })

  if (!healthData) {
    return null
  }

  return (
    <Box mb={6}>
      <Heading size="md" mb={4}>
        Sistema Status
      </Heading>
      <Grid templateColumns="repeat(auto-fit, minmax(250px, 1fr))" gap={4}>
        <Stat
          icon={getStatusIcon(healthData.status)}
          color={getStatusColor(healthData.status)}
          title="Overall Status"
        >
          {healthData.message}
        </Stat>
        <Stat
          icon={FaDatabase}
          color={getStatusColor(healthData.database)}
          title="Database"
        >
          {healthData.database === 'healthy' ? 'Connected' : 'Disconnected'}
        </Stat>
        {healthData.services.map((service) => (
          <Stat
            key={service.name}
            icon={getServiceIcon(service.name)}
            color={getStatusColor(service.status)}
            title={service.name}
          >
            {service.message ||
              (service.status === 'healthy' ? 'Available' : 'Unavailable')}
          </Stat>
        ))}
      </Grid>
    </Box>
  )
}
