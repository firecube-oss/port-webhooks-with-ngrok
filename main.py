from contextlib import asynccontextmanager
from os import getenv
from typing import Annotated

import ngrok
import uvicorn
from fastapi import FastAPI, Request
from loguru import logger

from port_api_core import PortClient
from port_runs_simulator import simulate_a_run

NGROK_AUTH_TOKEN = getenv("NGROK_AUTH_TOKEN", "")
NGROK_EDGE = getenv("NGROK_EDGE", "edge:edghts_")
PORT_CLIENT_ID = getenv("PORT_CLIENT_ID", "")
PORT_CLIENT_SECRET = getenv("PORT_CLIENT_SECRET", "")

APPLICATION_PORT = 5000


# ngrok free tier only allows one agent. So we tear down the tunnel on application termination
@asynccontextmanager
async def lifespan(app: FastAPI):
    PortClient.authenticate(clientId=PORT_CLIENT_ID, clientSecret=PORT_CLIENT_SECRET)
    logger.info("Setting up Ngrok Tunnel")
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    ngrok.forward(
        addr=APPLICATION_PORT,
        labels=NGROK_EDGE,
        proto="labeled",
        # Confirms https://docs.getport.io/create-self-service-experiences/security/
        allow_cidr="44.221.30.248/32,44.193.148.179/32,34.197.132.205/32,3.251.12.20/32",
    )
    yield
    logger.info("Tearing Down Ngrok Tunnel")
    ngrok.disconnect()


app = FastAPI(lifespan=lifespan)

#endpoint to send webhooks that doesn't do anything with them
@app.post("/manual")
async def root(request:Request):
    logger.info(f" Webhook invoked via / with RunID = {request.headers.get('run_id')}")
    return {}


# endpoint that will automatically send updates to Port
@app.post("/")
async def root(request:Request):
    logger.info(f" Webhook invoked via / with RunID = {request.headers.get('run_id')}")
    simulate_a_run(request.headers.get('run_id'))
    return {}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=APPLICATION_PORT, reload=True)
