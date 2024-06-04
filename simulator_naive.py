import random
import time
from os import getenv
from sys import argv

from faker import Faker
from fastapi import APIRouter, Request
from loguru import logger

from port_api_action_runs import (PortActionActionRunsUpdateFinal,
                                  PortActionRunsClient,
                                  PortActionRunsFinalStatus,
                                  PortActionRunsLogUpdate,
                                  PortActionRunsUpdate)
from port_api_core import PortClient


class NaiveSimulatorBlueprint:
    pass


class NaiveSimulatorEntity:
    pass


class NaiveSimulatorAction:
    pass


class ExpectedHeaders(PortActionsWebookHeadersBase):
    run_id: str


faker = Faker()
router = APIRouter(
    prefix="",
    tags=["naive"],
)


# endpoint to send webhooks that doesn't do anything with them
@router.post("/manual")
async def naive_simulator_manual(request: Request):
    parsed_header = ExpectedHeaders.model_validate(dict(request.headers.items()))
    logger.info(f" Webhook invoked via / with RunID = {parsed_header.run_id}")
    return {}


# endpoint that will automatically send updates to Port
@router.post("/")
async def naive_simulator_automatic(request: Request):
    parsed_header = ExpectedHeaders.model_validate(dict(request.headers.items()))
    logger.info(f" Webhook invoked via / with RunID = {parsed_header.run_id}")
    simulate_a_run(parsed_header.run_id)
    return {}


def simulate_a_run(run_id: str):
    client = PortActionRunsClient(run_id=run_id)
    # simulate an INITIALIZING phase
    client.send_status_update(
        PortActionRunsUpdate(
            run_id=run_id,
            statusLabel="INITIALIZING",
            summary=faker.paragraph(),
        )
    )
    for i in range(random.randint(1, 3)):
        client.send_log_update(
            PortActionRunsLogUpdate(
                message=f"INITIALIZING PHASE {i}:  {faker.paragraph()}",
                run_id=run_id,
            )
        )

        # wait a little to simulate making calls to APIs etc
    time.sleep(5)

    # we have begun Infrastructure as Code / CI/CD / Provisioning Scripts
    client.send_status_update(
        PortActionRunsUpdate(
            run_id=run_id,
            statusLabel="PROVISIONING with Provider",
            summary=faker.paragraph(),
            link=[faker.url(), faker.url()],
        )
    )
    for i in range(random.randint(1, 3)):
        client.send_log_update(
            PortActionRunsLogUpdate(
                run_id=run_id,
                message=f"PROVISIONING PHASE {i}:  {faker.paragraph()}",
            )
        )

    # Infrastructure as Code / CI/CD /Provisioning Scripts aren't always -- simulate a delay (e.g Terraform Plan, Gitlab Runners being Available .... etc etc )
    time.sleep(random.randint(10, 30))

    # Simulate Updates Infrastructure as Code / CI/CD / Provisioning Scripts
    for i in range(random.randint(1, 5)):
        client.send_status_update(
            PortActionRunsUpdate(
                run_id=run_id,
                statusLabel=f"UPDATES from Provider Phase {i}",
                summary=faker.paragraph(),
            )
        )
        client.send_log_update(
            PortActionRunsLogUpdate(
                message=f"UPDATES PHASE {i}:  {faker.paragraph()}",
                run_id=run_id,
            )
        )
        time.sleep(random.randint(5, 20))  # change this to your requirements

    client.send_final_update(
        PortActionActionRunsUpdateFinal(
            run_id=run_id,
            status=PortActionRunsFinalStatus.SUCCESS,
            summary=faker.paragraph(),
        )
    )


if __name__ == "__main__":
    PORT_CLIENT_ID = getenv("PORT_CLIENT_ID", "")
    PORT_CLIENT_SECRET = getenv("PORT_CLIENT_SECRET", "")
    PortClient.authenticate(clientId=PORT_CLIENT_ID, clientSecret=PORT_CLIENT_SECRET)
    client = PortActionRunsClient(run_id=argv[1])
    client.send_final_update(
        PortActionActionRunsUpdateFinal(
            run_id=argv[1],
            status=PortActionRunsFinalStatus.SUCCESS,
            summary=faker.paragraph(),
        )
    )
