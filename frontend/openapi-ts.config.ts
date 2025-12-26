import { defaultPlugins, defineConfig } from '@hey-api/openapi-ts'

export default defineConfig({
  client: '@hey-api/client-fetch',
  input: 'http://localhost:8001/api/openapi.json',
  output: {
    format: 'biome',
    lint: 'eslint',
    path: './src/client',
  },
  plugins: [
    ...defaultPlugins,
    '@hey-api/schemas',
    {
      dates: true,
      name: '@hey-api/transformers',
    },
    { name: '@hey-api/sdk', transformer: true },
    {
      enums: 'javascript',
      name: '@hey-api/typescript',
    },
    '@tanstack/react-query',
  ],
})
