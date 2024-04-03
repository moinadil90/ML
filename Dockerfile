# Use Alpine Linux as base image for certificates
FROM alpine:3 as certs
RUN apk update && apk add ca-certificates

# Build the binary
FROM golang:1.19-buster as builder
WORKDIR /app

# Set config for private repos
ARG GITHUB_TOKEN
RUN git config \
 --global \
 url."https://${GITHUB_TOKEN}@github.com".insteadOf \
 "https://github.com"

# Download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .
RUN go build -o feed-relevance-service .

# Build final image - glibc required to run go binary
FROM busybox:stable-glibc
WORKDIR /app
ARG BUILD_NUMBER
ENV BUILD_NUMBER=${BUILD_NUMBER:-LOCAL}

# Copy binary and config
COPY --from=builder /app/feed-relevance-service ./
COPY --from=builder /app/config config/
COPY --from=builder /app/asset asset/
COPY --from=builder /app/instrumentationConfig.yaml .

# Copy certificates from certs stage
COPY --from=certs /etc/ssl/certs /etc/ssl/certs

CMD ["./feed-relevance-service"]
