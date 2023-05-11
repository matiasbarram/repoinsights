#!/bin/bash

# Ejecutar extract.py en repoinsights-extract_service-1 en segundo plano
docker exec -d repoinsights-extract_service-1 python extract.py &

# Ejecutar extract.py en repoinsights-extract_service-2 en segundo plano
docker exec -d repoinsights-extract_service-2 python extract.py &
