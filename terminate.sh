#!/bin/bash
source <(grep = config.ini)
kill -9 `lsof -t -i:$GRPC_PORT`
# kill -9 `lsof -t -i:$MQTT_PORT`
# kill -9 `lsof -t -i:$REST_PORT`


