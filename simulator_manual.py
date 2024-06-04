from fastapi import APIRouter, Request
from loguru import logger

from port_api_action_runs import PortActionsWebookHeadersBase

router = APIRouter(
    prefix="",
    tags=["manual"],
)


class ManualSimulatorExpectedHeaders(PortActionsWebookHeadersBase):
    run_id: str


# endpoint to send webhooks that doesn't do anything with them
@router.post("/manual")
async def naive_simulator_manual(request: Request):
    parsed_header = ManualSimulatorExpectedHeaders.model_validate(
        dict(request.headers.items())
    )
    logger.info(f" Webhook invoked via / with RunID = {parsed_header.run_id}")
    return {}
