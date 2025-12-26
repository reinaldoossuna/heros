import { HStack, Separator as SeparatorChakra, Text } from '@chakra-ui/react'

const Separator = ({ label }: { label: string }) => (
  <HStack>
    <Text flexShrink="0" fontWeight={'bold'}>
      {label}
    </Text>
    <SeparatorChakra colorPalette={'blue'} />
  </HStack>
)

export default Separator
