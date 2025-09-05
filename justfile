
[working-directory: 'frontend']
front:
    npx vite


[working-directory: 'frontend']
openapi:
    npm run openapi

[working-directory: 'backend']
back:
    uv run heros-server --port 8001 --log_level debug
