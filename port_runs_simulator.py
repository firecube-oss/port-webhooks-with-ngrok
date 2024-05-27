import random
import time

from faker import Faker

from port_api_runs import *

faker = Faker()


def simulate_a_run(runID: str):

    # simulate an INITIALIZING phase
    send_status_update(
        PortActionActionRunUpdate(
            runID=runID,
            statusLabel="INITIALIZING",
            summary=faker.paragraph(),
        )
    )
    for i in range(random.randint(1, 3)):
        send_log_update(
            PortActionRunLogUpdate(
                message=f"INITIALIZING PHASE {i}:  {faker.paragraph()}",
                runID=runID,
            )
        )

    # wait a little to simulate making calls to APIs etc
    time.sleep(5)

    # we have begun Infrastructure as Code / CI/CD / Provisioning Scripts
    send_status_update(
        PortActionActionRunUpdate(
            runID=runID,
            statusLabel="PROVISIONING with Provider",
            summary=faker.paragraph(),
            link=[faker.url(), faker.url()],
        )
    )
    for i in range(random.randint(1, 3)):
        send_log_update(
            PortActionRunLogUpdate(
                runID=runID,
                message=f"PROVISIONING PHASE {i}:  {faker.paragraph()}",
            )
        )

    # Infrastructure as Code / CI/CD /Provisioning Scripts aren't always -- simulate a delay (e.g Terraform Plan, Gitlab Runners being Available .... etc etc )
    time.sleep(random.randint(10, 30))

    # Simulate Updates Infrastructure as Code / CI/CD / Provisioning Scripts
    for i in range(random.randint(1, 5)):
        send_status_update(
            PortActionActionRunUpdate(
                runID=runID,
                statusLabel=f"UPDATES from Provider Phase {i}",
                summary=faker.paragraph(),
            )
        )
        send_log_update(
            PortActionRunLogUpdate(
                message=f"UPDATES PHASE {i}:  {faker.paragraph()}",
                runID=runID,
            )
        )
        time.sleep(random.randint(5, 20))  # change this to your requirements

    send_final_update(
        PortActionActionLRunUpdateFinal(
            runID=runID,
            status=PortActionRunFinalStatus.SUCCESS,
            summary=faker.paragraph(),
        )
    )
