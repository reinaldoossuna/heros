import { createFileRoute } from '@tanstack/react-router'
import { Box, Heading } from '@chakra-ui/react'
import CredentialsManager from '../../components/credentials/CredentialsManager'

export const Route = createFileRoute('/_layout/credentials')({
  component: CredentialsPage,
})

function CredentialsPage() {
  return (
    <Box maxH={'100vh'} pt={12} m={4}>
      <Heading size={'2xl'} mb={8}>
        API Credentials Management
      </Heading>
      <CredentialsManager />
    </Box>
  )
}
