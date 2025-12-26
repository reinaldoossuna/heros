import { Box, Flex, Image, Text } from '@chakra-ui/react'
import HerosLogo from '../../assets/heros.jpg'

import SidebarItems from './SidebarItems'

export default function Sidebar() {
  return (
    <Box p={3} h="100vh" position={'sticky'} top="0" display={'flex'}>
      <Flex
        flexDir="column"
        justify={'space-between'}
        p={4}
        borderRadius={12}
        background={'var(--main)'}
      >
        <Box>
          <Image src={HerosLogo} alt="Logo" w="180px" maxW="2xs" p={6} />
          <SidebarItems />
        </Box>
        <Text fontSize="sm" p={2} maxW="180px">
          Sistema de Monitoramento Hidrológico e Meteorológico
        </Text>
      </Flex>
    </Box>
  )
}
