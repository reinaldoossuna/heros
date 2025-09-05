import { Box, Heading, Separator } from '@chakra-ui/react';
import { ReactNode } from 'react';

type RChildren = {
    children: ReactNode
}
const LayoutBox = ({ children }: RChildren) => (

    <Box maxH={"100vh"} pt={12} m={4}>
        {children}
    </Box>


);

LayoutBox.Title = (props: RChildren) => (
    <>
        <Heading size={"7xl"}>{props.children}</Heading>
        <Separator colorPalette={"blue"} size={"xs"} margin={5} />
    </>
)

export default LayoutBox;
