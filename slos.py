import click
import json
import logging
import sys

from datadog_api_client import ApiClient
from datadog_api_client import Configuration
from datadog_api_client.v1.api.service_level_objectives_api import (
    ServiceLevelObjectivesApi,
)
from datadog_api_client.v1.api.service_level_objectives_api import ServiceLevelObjective
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _filter_by_monitor(
    slos: list[ServiceLevelObjective], monitor_id: int
) -> list[ServiceLevelObjective]:
    return list(filter(lambda slo: monitor_id in getattr(slo, "monitor_ids", []), slos))


@click.command(context_settings={"auto_envvar_prefix": "SLOS", "show_default": True})
@click.option("--monitor-id", "-m", help="Monitor ID to get SLOs related", type=int)
@click.option("--datadog-api-key", help="Datadog API key", type=str, show_envvar=True)
@click.option("--datadog-app-key", help="Datadog APP key", type=str, show_envvar=True)
@click.option(
    "--pretty/--no-pretty",
    "-p",
    help="Pretty output",
    type=bool,
    is_flag=True,
    default=False,
    show_envvar=True,
)
@click.option(
    "--debug/--no-debug",
    "-v",
    help="Debug logging",
    type=bool,
    is_flag=True,
    default=False,
    show_envvar=True,
)
def main(
    monitor_id: int,
    datadog_api_key: str,
    datadog_app_key: str,
    pretty: bool,
    debug: bool,
) -> None:
    assert sys.version_info >= (3, 9), "Script requires Python 3.9+"

    if debug:
        logger.setLevel(logging.DEBUG)

    configuration: Configuration = Configuration()
    logger.debug("Creating Datadog client")
    configuration.api_key["apiKeyAuth"] = datadog_api_key
    configuration.api_key["appKeyAuth"] = datadog_app_key
    slo_client: Optional[ServiceLevelObjectivesApi] = None
    with ApiClient(configuration=configuration) as client:
        slo_client = ServiceLevelObjectivesApi(api_client=client)

    logger.debug("Getting all SLOs from Datadog")
    slos: list[ServiceLevelObjective] = slo_client.list_slos()["data"]
    logger.debug("Keeping all SLOs that have monitor with id '%s'", monitor_id)
    slos = _filter_by_monitor(slos, monitor_id)

    indent: Optional[int] = 2 if pretty else None
    logger.debug("Printing output")
    print(json.dumps(list(map(lambda slo: slo.to_dict(), slos)), indent=indent))


if __name__ == "__main__":
    main()
