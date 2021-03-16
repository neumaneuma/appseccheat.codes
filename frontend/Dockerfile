FROM node:15-alpine

WORKDIR /app

COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm install
COPY . .

CMD ["npm", "run", "dev"]
