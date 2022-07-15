"""
Prometheus collectors for AudioCodes SBC.
"""

from prometheus_client.core import GaugeMetricFamily
from requests import Session

from audiocodes_exporter.helpers import camel_to_snake, fetch


class PortStatsCollector:
    """
    Collects AudioCodes SBC port statistics from the API endpoint
    """

    def __init__(self, api_host: str, api_session: Session) -> None:
        self._api_host = api_host
        self._api_session = api_session

    def collect(self):
        port_ids = fetch(
            api_host=self._api_host,
            api_session=self._api_session,
            api_endpoint="/kpi/current/network/portStats/port",
        )

        data = fetch(
            api_host=self._api_host,
            api_session=self._api_session,
            api_endpoint="/kpi/current/network/portStats/port/0",
        )

        metrics = {}

        for item in data["items"]:
            # Create the metric families based on the ID's of the API response for the global metrics
            metrics[item["id"]] = GaugeMetricFamily(
                camel_to_snake(item["id"]), item["description"], labels=["port"]
            )

        for port in port_ids["items"]:
            data = fetch(
                api_host=self._api_host,
                api_session=self._api_session,
                api_endpoint=f"/kpi/current/network/portStats/port/{port['id']}",
            )
            for item in data["items"]:
                if not item["value"] is None:
                    metrics[item["id"]].add_metric(
                        labels=[f"port{port['id']}"], value=item["value"]
                    )
        for k, v in metrics.items():
            yield v
