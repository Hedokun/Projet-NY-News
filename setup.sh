#!/bin/bash
docker pull elasticsearch
docker pull kibana
docker pull datascientestnyt/api_nyt:latest
docker pull datascientestnyt/front_nyt:latest

docker compose up -d docker-compose.yml
