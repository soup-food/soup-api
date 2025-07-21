# soup-api

A simple API built by some firends with **FastAPI** at its core built to serve the Soup Food project.
A full stack application that includes this API, MongoDB for data storage, and Nginx for serving static files and reverse proxying is available on [GitHub](https://github.com/soup-food/soup-compose) repository.

## Quick Start

Using [uv](https://docs.astral.sh/uv/) as package menager. 

```bash
uv sync
```

```bash
uv run uvicorn soup_food.main:api --host 0.0.0.0 --port 8000
```

## From Doker Image

To run the Soup API using Docker, you can pull the pre-built image from GitHub Container Registry:

```bash
docker pull ghcr.io/soup-food/soup-api
```

Then, run the container with the following command:

```bash
docker run -p 8000:8000 ghcr.io/soup-food/soup-api
```