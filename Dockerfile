FROM node:17.7
WORKDIR /bot
COPY . .

RUN npm install

CMD node ./index.js

