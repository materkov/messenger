FROM node:10.9.0-alpine
COPY . .
RUN npm install && npm run build

FROM nginx:1.15.2-alpine
COPY --from=0 build/ /usr/share/nginx/html
