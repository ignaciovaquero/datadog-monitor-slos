import pytest
from slos import _filter_by_monitor

from datadog_api_client.v1.api.service_level_objectives_api import ServiceLevelObjective
from datadog_api_client.v1.model.slo_threshold import SLOThreshold
from datadog_api_client.v1.model.slo_timeframe import SLOTimeframe
from datadog_api_client.v1.model.slo_type import SLOType
from datadog_api_client.v1.model.service_level_objective_query import (
    ServiceLevelObjectiveQuery,
)


def _monitor_slos(params: dict[str, list[int]]) -> list[ServiceLevelObjective]:
    slos: list[ServiceLevelObjective] = []
    for name, monitors in params.items():
        slos.append(
            ServiceLevelObjective(
                name=name,
                thresholds=[
                    SLOThreshold(target=99.9, timeframe=SLOTimeframe(value="7d"))
                ],
                type=SLOType("monitor"),
                monitor_ids=monitors,
            )
        )
    return slos


def _metric_slos(names: list[str]) -> list[ServiceLevelObjective]:
    slos: list[ServiceLevelObjective] = []
    for name in names:
        slos.append(
            ServiceLevelObjective(
                name=name,
                thresholds=[
                    SLOThreshold(target=99.9, timeframe=SLOTimeframe(value="7d"))
                ],
                type=SLOType("metric"),
                query=ServiceLevelObjectiveQuery("", ""),
            )
        )
    return slos


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            {"slos": _monitor_slos({"slo_1": [1, 2, 3]}), "monitor_id": -1},
            _monitor_slos({"slo_1": [1, 2, 3]}),
        ),
        (
            {"slos": _monitor_slos({"slo_1": [1, 2, 3]}), "monitor_id": 4},
            [],
        ),
        (
            {"slos": _monitor_slos({"slo_1": [1, 2, 3]}), "monitor_id": 1},
            _monitor_slos({"slo_1": [1, 2, 3]}),
        ),
        (
            {
                "slos": _monitor_slos({"slo_1": [1, 2, 3], "slo_2": [2, 3]}),
                "monitor_id": 1,
            },
            _monitor_slos({"slo_1": [1, 2, 3]}),
        ),
        (
            {
                "slos": _monitor_slos({"slo_1": [1, 2, 3], "slo_2": [2, 3]}),
                "monitor_id": 2,
            },
            _monitor_slos({"slo_1": [1, 2, 3], "slo_2": [2, 3]}),
        ),
        (
            {
                "slos": _monitor_slos({"slo_1": [1, 2, 3], "slo_2": [2, 3, 4]}),
                "monitor_id": 4,
            },
            _monitor_slos({"slo_2": [2, 3, 4]}),
        ),
        (
            {
                "slos": _metric_slos(["slo_1", "slo_2"]),
                "monitor_id": 4,
            },
            [],
        ),
        (
            {
                "slos": _metric_slos(["slo_1", "slo_2"]),
                "monitor_id": -1,
            },
            _metric_slos(["slo_1", "slo_2"]),
        ),
    ],
)
def test_filter_by_monitor(input, expected):
    got: list[ServiceLevelObjective] = _filter_by_monitor(**input)
    assert expected == got, f"expected: {expected}, got: {got}"
