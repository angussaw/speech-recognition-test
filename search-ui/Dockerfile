FROM node:18

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install

COPY . .

RUN yarn add @elastic/search-ui-elasticsearch-connector

EXPOSE 3000

CMD ["yarn", "start"]
