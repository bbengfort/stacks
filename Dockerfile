# Build Go API Server
FROM golang:latest as build-api
RUN mkdir -p /go/src/github.com/bbengfort/stacks
RUN go get -u github.com/golang/dep/cmd/dep

WORKDIR /go/src/github.com/bbengfort/stacks
COPY ./api ./api
WORKDIR /go/src/github.com/bbengfort/stacks/api
RUN dep ensure
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o /go/bin/stacks ./cmd/stacks/main.go

# Build Vue Web Client
FROM node:11.12.0-alpine as build-web
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./web/package*.json ./
RUN npm install
COPY ./web .
RUN npm run build

# Production
FROM nginx:stable as production
WORKDIR /app
COPY --from=build-web /app/dist /usr/share/nginx/html
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build-api /go/bin/stacks /usr/local/bin/stacks
COPY ./nginx/entrypoint.sh entrypoint.sh
CMD ./entrypoint.sh