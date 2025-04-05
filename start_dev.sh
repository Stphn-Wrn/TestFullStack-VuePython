#!/bin/bash
docker compose --env-file ./backend/environment/.compose.env up  --build -d
cd backend
poetry install