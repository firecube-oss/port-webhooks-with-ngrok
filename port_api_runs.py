from enum import Enum

import requests
from loguru import logger
from pydantic import AnyUrl, BaseModel

from port_api_core import PortClient

API_RUNS_URL = f"{PortClient.API_BASE_URL}/actions/runs"
API_HEADERS = PortClient.API_HEADERS


# Base Model for all messages to include runID
class PortActionRunBase(BaseModel):
    runID: str


# https://api.getport.io/static/index.html#/Action%20Runs/patch_v1_actions_runs__run_id_
class PortActionRunFinalStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class PortActionActionRunUpdate(PortActionRunBase):
    summary: str | None = None
    statusLabel: str | None = None
    link: list[AnyUrl] | None = None
    externalRunId: str | None = None


class PortActionActionLRunUpdateFinal(PortActionActionRunUpdate):
    status: PortActionRunFinalStatus


# https://api.getport.io/static/index.html#/Action%20Runs/get_v1_actions_runs__run_id__logs
class PortActionRunLogUpdate(PortActionRunBase):
    message: str


def prepare_port_api_payload(message) -> str:
    return message.model_dump_json(exclude_none=True, exclude="runID")


# debugging sucks so hopefully this provides some context
def log_port_api_response(raw_response: requests.models.Response):
    if raw_response.status_code < 300:
        logger.info("API Call Successful")
    else:
        logger.error(
            f"Status Code: {raw_response.status_code} Message: {raw_response.text}"
        )


def send_log_update(message: PortActionRunLogUpdate) -> str:
    raw_response = requests.post(
        url=f"{API_RUNS_URL}/{message.runID}/logs",
        headers=API_HEADERS,
        data=prepare_port_api_payload(message),
    )
    log_port_api_response(raw_response)


def send_status_update(message: PortActionActionRunUpdate) -> str:
    raw_response = requests.patch(
        url=f"{API_RUNS_URL}/{message.runID}",
        headers=API_HEADERS,
        data=prepare_port_api_payload(message),
    )
    log_port_api_response(raw_response)


def send_final_update(message: PortActionActionLRunUpdateFinal) -> str:
    raw_response = requests.patch(
        url=f"{API_RUNS_URL}/{message.runID}",
        headers=API_HEADERS,
        data=prepare_port_api_payload(message),
    )
    log_port_api_response(raw_response)
