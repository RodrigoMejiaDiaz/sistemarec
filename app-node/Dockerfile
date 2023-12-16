FROM node:alpine

RUN mkdir -p /opt/app

WORKDIR /opt/app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3001

CMD [ "npm", "start"]