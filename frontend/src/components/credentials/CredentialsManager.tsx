import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  Box,
  Button,
  Input,
  VStack,
  HStack,
  Text,
  Heading,
  Grid,
  GridItem,
  Flex,
} from '@chakra-ui/react'
import {
  listServicesApiCredentialsServicesGetOptions,
  updateCredentialApiCredentialsUpdatePostMutation,
} from '../../client/@tanstack/react-query.gen'

interface Service {
  service_name: string
  username: string
  is_active: boolean
  last_updated: string
  updated_by?: string
}

interface UpdateResponse {
  success: boolean
  message: string
  service_name: string
  updated_at: Date
  updated_by: string
}

export default function CredentialsManager() {
  const queryClient = useQueryClient()
  const [selectedService, setSelectedService] = useState<string>('')
  const [username, setUsername] = useState<string>('')
  const [password, setPassword] = useState<string>('')
  const [confirmPassword, setConfirmPassword] = useState<string>('')
  const [error, setError] = useState<string>('')
  const [success, setSuccess] = useState<string>('')

  // Fetch services using OpenAPI generated hook
  const { data: servicesData, isLoading: servicesLoading } = useQuery(
    listServicesApiCredentialsServicesGetOptions()
  )

  const services: Service[] = (servicesData?.services as Service[]) ?? []

  // Set first service as selected when services load
  if (services.length > 0 && !selectedService) {
    setSelectedService(services[0].service_name)
  }

  // Mutation for updating credentials
  const updateMutation = useMutation({
    mutationFn: updateCredentialApiCredentialsUpdatePostMutation().mutationFn,
    onSuccess: (result: UpdateResponse) => {
      setSuccess(
        `✓ Credentials updated successfully at ${new Date(result.updated_at).toLocaleString()}`
      )
      setUsername('')
      setPassword('')
      setConfirmPassword('')
      // Refetch services to get updated list
      queryClient.invalidateQueries(
        listServicesApiCredentialsServicesGetOptions()
      )
    },
    onError: (err: any) => {
      const errorMessage =
        err?.response?.data?.detail || 'Failed to update credentials'
      setError(errorMessage)
    },
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (!selectedService || !username || !password) {
      setError('All fields are required')
      return
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    updateMutation.mutate({
      body: {
        service_name: selectedService,
        username,
        password,
      },
    })
  }

  if (servicesLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" h="200px">
        <Text>Loading...</Text>
      </Box>
    )
  }

  return (
    <Grid templateColumns={{ base: '1fr', lg: '1fr 1fr' }} gap={8}>
      {/* Services List */}
      <GridItem>
        <Box borderWidth="1px" borderRadius="lg" p={4} mb={4}>
          <Heading size="md" mb={4}>
            Configured Services
          </Heading>

          {services.length === 0 ? (
            <Text color="gray.500">No services configured</Text>
          ) : (
            <VStack align="stretch" gap={2}>
              {services.map((service) => (
                <Box
                  key={service.service_name}
                  p={3}
                  borderWidth="1px"
                  borderRadius="md"
                  cursor="pointer"
                  bg={
                    selectedService === service.service_name
                      ? 'blue.50'
                      : 'white'
                  }
                  onClick={() => setSelectedService(service.service_name)}
                  _hover={{ bg: 'gray.50' }}
                >
                  <Flex justify="space-between" align="center">
                    <Box>
                      <Text fontWeight="bold">
                        {service.service_name.toUpperCase()}
                      </Text>
                      <Text fontSize="sm" color="gray.600">
                        {service.username}
                      </Text>
                    </Box>
                    <Box
                      px={2}
                      py={1}
                      bg={service.is_active ? 'green.100' : 'red.100'}
                      color={service.is_active ? 'green.800' : 'red.800'}
                      borderRadius="md"
                      fontSize="xs"
                    >
                      {service.is_active ? 'Active' : 'Inactive'}
                    </Box>
                  </Flex>
                </Box>
              ))}
            </VStack>
          )}
        </Box>

        {selectedService && (
          <Box borderWidth="1px" borderRadius="lg" p={4}>
            <Heading size="sm" mb={4}>
              {selectedService.toUpperCase()} Details
            </Heading>

            {services
              .filter((s) => s.service_name === selectedService)
              .map((service) => (
                <VStack align="start" gap={3} key={service.service_name}>
                  <Box>
                    <Text fontSize="sm" color="gray.600">
                      Username
                    </Text>
                    <Text fontWeight="bold">{service.username}</Text>
                  </Box>
                  <Box>
                    <Text fontSize="sm" color="gray.600">
                      Last Updated
                    </Text>
                    <Text fontWeight="bold">
                      {new Date(service.last_updated).toLocaleString()}
                    </Text>
                  </Box>
                  {service.updated_by && (
                    <Box>
                      <Text fontSize="sm" color="gray.600">
                        Updated By
                      </Text>
                      <Text fontWeight="bold">{service.updated_by}</Text>
                    </Box>
                  )}
                </VStack>
              ))}
          </Box>
        )}
      </GridItem>

      {/* Update Form */}
      <GridItem>
        <Box borderWidth="1px" borderRadius="lg" p={4}>
          <Heading size="md" mb={4}>
            Update Credentials
          </Heading>

          <form onSubmit={handleSubmit}>
            <VStack gap={4}>
              {error && (
                <Box
                  bg="red.50"
                  p={3}
                  borderRadius="md"
                  borderLeftWidth="4px"
                  borderLeftColor="red.500"
                  w="100%"
                >
                  <Text color="red.700" fontSize="sm">
                    <strong>Error:</strong> {error}
                  </Text>
                </Box>
              )}

              {success && (
                <Box
                  bg="green.50"
                  p={3}
                  borderRadius="md"
                  borderLeftWidth="4px"
                  borderLeftColor="green.500"
                  w="100%"
                >
                  <Text color="green.700" fontSize="sm">
                    {success}
                  </Text>
                </Box>
              )}

              <Box w="100%">
                <Text fontSize="sm" fontWeight="bold" mb={1}>
                  Service
                </Text>
                <Input
                  type="text"
                  value={selectedService}
                  readOnly
                  bg="gray.100"
                  cursor="not-allowed"
                />
              </Box>

              <Box w="100%">
                <Text fontSize="sm" fontWeight="bold" mb={1}>
                  Username
                </Text>
                <Input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Enter new username"
                  disabled={updateMutation.isPending}
                />
              </Box>

              <Box w="100%">
                <Text fontSize="sm" fontWeight="bold" mb={1}>
                  Password
                </Text>
                <Input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter new password"
                  disabled={updateMutation.isPending}
                />
              </Box>

              <Box w="100%">
                <Text fontSize="sm" fontWeight="bold" mb={1}>
                  Confirm Password
                </Text>
                <Input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Confirm password"
                  disabled={updateMutation.isPending}
                />
              </Box>

              <HStack gap={4} w="100%">
                <Button
                  type="submit"
                  colorScheme="blue"
                  loading={updateMutation.isPending}
                  disabled={updateMutation.isPending}
                  flex={1}
                >
                  Update Credentials
                </Button>
                <Button
                  variant="outline"
                  onClick={() => {
                    setUsername('')
                    setPassword('')
                    setConfirmPassword('')
                    setError('')
                  }}
                  disabled={updateMutation.isPending}
                  flex={1}
                >
                  Clear
                </Button>
              </HStack>

              <Box
                bg="blue.50"
                p={3}
                borderRadius="md"
                borderLeftWidth="4px"
                borderLeftColor="blue.500"
                w="100%"
              >
                <Text color="blue.700" fontSize="sm">
                  <strong>Note:</strong> New credentials will be used
                  immediately on the next API request. No server restart
                  required.
                </Text>
              </Box>
            </VStack>
          </form>
        </Box>
      </GridItem>
    </Grid>
  )
}
