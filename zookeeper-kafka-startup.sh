#!/bin/bash 

# Startup zookeeper and kafka cluster
echo "Starting up zookeeper and kafka clusters.."
echo "Composing.."

sudo docker-compose -f docker-compose.yml up -d 
docker ps 
