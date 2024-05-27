from enum import Enum

from loguru import logger
from pydantic import AnyUrl, BaseModel

from port_api_core import PortClient


# base model for for requests going to Runs API
class PortActionRunsRequestBase(BaseModel):
    pass


# https://api.getport.io/static/index.html#/Action%20Runs/patch_v1_actions_runs__run_id_
class PortActionRunsFinalStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class PortActionRunsUpdate(PortActionRunsRequestBase):
    summary: str | None = None
    statusLabel: str | None = None
    link: list[AnyUrl] | None = None
    externalRunId: str | None = None


class PortActionActionRunsUpdateFinal(PortActionRunsUpdate):
    status: PortActionRunsFinalStatus


# https://api.getport.io/static/index.html#/Action%20Runs/get_v1_actions_runs__run_id__logs
class PortActionRunsLogUpdate(PortActionRunsRequestBase):
    message: str


class PortActionRunsClient:
    def __init__(self, run_id) -> None:
        self._client = PortClient(exclude_pydantic_fields="run_id")
        self._API_URL = f"{PortClient.API_BASE_URL}/actions/runs/{run_id}"
        self._run_id = run_id

    def send_log_update(self, body: PortActionRunsLogUpdate) -> str:
        self._client.post(url=f"{self._API_URL}/logs", body=body)

    def send_status_update(self, body: PortActionRunsUpdate) -> str:
        self._client.patch(url=f"{self._API_URL}", body=body)

    def send_final_update(self, body: PortActionActionRunsUpdateFinal) -> str:
        self._client.patch(url=f"{self._API_URL}", body=body)
