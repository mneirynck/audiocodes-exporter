"""
Prometheus collectors for AudioCodes SBC.
"""

from prometheus_client.core import GaugeMetricFamily
from requests import Session

from helpers import camel_to_snake, fetch


class CpuStatsCollector:
    """
    Collects AudioCodes SBC cpu statistics from the API endpoint
    """

    def __init__(self, api_host: str, api_session: Session) -> None:
        self._api_host = api_host
        self._api_session = api_session

    def collect(self):
        cpu_ids = fetch(
            self._api_host, self._api_session, "/kpi/current/system/cpuStats/cpu"
        )

        data = fetch(
            api_host=self._api_host,
            api_session=self._api_session,
            api_endpoint="/kpi/current/system/cpuStats/cpu/0",
        )

        metrics = {}

        for item in data["items"]:
            # Create the metric families based on the ID's of the API response for the global metrics
            metrics[item["id"]] = GaugeMetricFamily(
                camel_to_snake(item["id"]), item["description"], labels=["cpu"]
            )

        for cpu in cpu_ids["items"]:
            data = fetch(
                self._api_host,
                self._api_session,
                f"/kpi/current/system/cpuStats/cpu/{cpu['id']}",
            )
            for item in data["items"]:
                if not item["value"] is None:
                    metrics[item["id"]].add_metric(
                        labels=[cpu["name"]], value=item["value"]
                    )

        for k, v in metrics.items():
            yield v
