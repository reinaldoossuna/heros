import { defineConfig } from '@chakra-ui/react'

const config = defineConfig({
  theme: {
    tokens: {
      colors: {
        main: { value: '#009688' },
        secondary: { value: '#EDF2F7' },
        success: { value: '#48BB78' },
        danger: { value: '#E53E3E' },
        light: { value: '#FAFAFA' },
        dark: { value: '#1A202C' },
        darkSlate: { value: '#252D3D' },
        dim: { value: '#A0AEC0' },
      },
    },
  },
})

export default config
