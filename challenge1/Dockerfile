FROM node:23-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY tsconfig.json ./

COPY src ./src

COPY *.xlsx ./

RUN npm run build

CMD ["npm", "start"]