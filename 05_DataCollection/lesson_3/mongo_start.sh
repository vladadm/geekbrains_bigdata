#!/bin/bash

# Dump
# docker exec some-mongo sh -c 'exec mongodump -d <database_name> --archive' > /some/path/on/your/host/all-collections.archive

# Start DB
docker run -d --name mongodb \
    -v $(pwd)/datadir:/data/db \
    -p 27017:27017 \
    -e MONGO_INITDB_ROOT_USERNAME=admin \
    -e MONGO_INITDB_ROOT_PASSWORD=admin \
    mongo

# Execute command on DB
#docker run -it --rm mongo \
#    mongo --host some-mon \
#        -u mongoadmin \
#        -p secret \
#        --authenticationDatabase admin \
#        some-db
