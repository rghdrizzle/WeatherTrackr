FROM golang:1.21-alpine3.18 AS build
WORKDIR /usr/src/app

COPY go.mod .

RUN go mod download

COPY . .
COPY .apiConfig ./

RUN go build -o weathertrakr


FROM scratch

COPY --from=build /usr/src/app .

EXPOSE 8080
CMD ["/weathertrakr"]