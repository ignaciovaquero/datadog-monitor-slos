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


def _filter_by_monitors(
    slos: list[ServiceLevelObjective], monitor_ids: tuple[int]
) -> list[ServiceLevelObjective]:
    if not monitor_ids:
        return slos
    logger.debug("filtering SLOs by monitor IDs '%s'", monitor_ids)
    monitor_ids_set = set(monitor_ids)
    return list(
        filter(
            lambda slo: monitor_ids_set.intersection(
                set(getattr(slo, "monitor_ids", []))
            ),
            slos,
        )
    )


@click.command(context_settings={"auto_envvar_prefix": "SLOS", "show_default": True})
@click.option(
    "--monitor-ids",
    "-m",
    multiple=True,
    default=[],
    help="Monitor IDs to get SLOs related. If not set, it returns all the SLOs found.",
    type=int,
)
@click.option(
    "--slo-ids",
    "-i",
    multiple=True,
    default=[],
    help="Get only SLOs with IDs specified.",
    type=str,
)
@click.option(
    "--datadog-api-key",
    help="Datadog API key.",
    type=str,
    required=True,
    show_envvar=True,
)
@click.option(
    "--datadog-app-key",
    help="Datadog APP key.",
    type=str,
    required=True,
    show_envvar=True,
)
@click.option(
    "--tags-query",
    "-q",
    help="Datadog tags query for querying the SLOs.",
    type=str,
    default="",
    show_envvar=True,
)
@click.option(
    "--pretty/--no-pretty",
    "-p",
    help="Pretty output.",
    type=bool,
    is_flag=True,
    default=False,
    show_envvar=True,
)
@click.option(
    "--debug/--no-debug",
    "-v",
    help="Debug logging.",
    type=bool,
    is_flag=True,
    default=False,
    show_envvar=True,
)
def main(
    monitor_ids: tuple[int],
    slo_ids: tuple[str],
    datadog_api_key: str,
    datadog_app_key: str,
    tags_query: str,
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
    slos: list[ServiceLevelObjective] = []
    slos = slo_client.list_slos(ids=",".join(slo_ids), tags_query=tags_query)["data"]
    slos = _filter_by_monitors(slos, monitor_ids)

    indent: Optional[int] = 2 if pretty else None
    logger.debug("Printing output")
    print(json.dumps(list(map(lambda slo: slo.to_dict(), slos)), indent=indent))


if __name__ == "__main__":
    main()
