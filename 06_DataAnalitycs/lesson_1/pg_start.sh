#!/bin/sh

docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=123 -e POSTGRES_HOST_AUTH_METHOD=trust -e POSTGRES_DB=analytics  -d postgres
