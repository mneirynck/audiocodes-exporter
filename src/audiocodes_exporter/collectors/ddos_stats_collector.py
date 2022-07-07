"""
Prometheus collectors for AudioCodes SBC.
"""

from prometheus_client.core import GaugeMetricFamily
from requests import Session

from helpers import camel_to_snake, fetch


class DdosStatsCollector:
    """
    Collects AudioCodes SBC ddos statistics from the API endpoint
    """

    def __init__(self, api_host: str, api_session: Session) -> None:
        self._api_host = api_host
        self._api_session = api_session

    def collect(self):
        global_data = fetch(
            api_host=self._api_host,
            api_session=self._api_session,
            api_endpoint="/kpi/current/network/ddosStats/global",
        )

        metrics = {}

        for item in global_data["items"]:
            # Create the metric families based on the ID's of the API response for the global metrics
            metrics[item["id"]] = GaugeMetricFamily(
                camel_to_snake(item["id"]), item["description"], labels=["entity"]
            )

            if not item["value"] is None:
                metric_id = item["id"]

                # Add the metrics to the family since we have the data already
                metrics[metric_id].add_metric(labels=["global"], value=item["value"])

        for k, v in metrics.items():
            yield v
