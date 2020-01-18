FROM node:12.7-alpine AS build
WORKDIR /app
COPY package.json /app/package.json
ENV PATH /app/node_modules/.bin:$PATH
RUN npm install
RUN npm install -g @angular/cli@7.3.9
RUN npm install @angular/cdk
COPY .  /app
CMD ng serve --host 0.0.0.0
