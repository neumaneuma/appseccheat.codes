FROM node:22.11.0-alpine

WORKDIR /frontend

EXPOSE 12300

COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm install --production=false

COPY . .
