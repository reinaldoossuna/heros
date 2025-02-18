# Build stage
FROM  node:20 as build

WORKDIR /app

COPY package*.json package-lock.json /app/

RUN npm install

COPY ./ /app/

RUN npm run build

# production
FROM nginx:1

COPY --from=build     /app/dist             /usr/share/nginx/html
COPY                  ./nginx.conf          /etc/nginx/conf.d/default.conf
