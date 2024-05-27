from enum import Enum

from loguru import logger
from pydantic import AnyUrl, BaseModel

from port_api_core import PortClient

runs_client = PortClient(exclude_pydantic_fields="runID")

API_RUNS_URL = f"{PortClient.API_BASE_URL}/actions/runs"
API_HEADERS = PortClient.API_HEADERS


# Base Model for all bodys to include runID
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


def send_log_update(body: PortActionRunLogUpdate) -> str:
    runs_client.post(url=f"{API_RUNS_URL}/{body.runID}/logs", body=body)


def send_status_update(body: PortActionActionRunUpdate) -> str:
    runs_client.patch(url=f"{API_RUNS_URL}/{body.runID}", body=body)


def send_final_update(body: PortActionActionLRunUpdateFinal) -> str:
    runs_client.patch(url=f"{API_RUNS_URL}/{body.runID}", body=body)
