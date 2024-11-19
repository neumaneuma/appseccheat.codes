FROM node:22.11.0

WORKDIR /frontend

EXPOSE 12300

COPY package.json package.json
RUN npm install

COPY . .
