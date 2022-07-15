"""
Prometheus collectors for AudioCodes SBC.
"""

from prometheus_client.core import GaugeMetricFamily
from requests import Session

from audiocodes_exporter.helpers import camel_to_snake, fetch


class StorageStatsCollector:
    """
    Collects AudioCodes SBC storage statistics from the API endpoint
    """

    def __init__(self, api_host: str, api_session: Session) -> None:
        self._api_host = api_host
        self._api_session = api_session

    def collect(self):
        partition_ids = fetch(
            self._api_host,
            self._api_session,
            "/kpi/current/system/storageStats/partition",
        )

        data = fetch(
            api_host=self._api_host,
            api_session=self._api_session,
            api_endpoint="/kpi/current/system/storageStats/partition/0",
        )

        metrics = {}

        for item in data["items"]:
            # Create the metric families based on the ID's of the API response for the global metrics
            metrics[item["id"]] = GaugeMetricFamily(
                camel_to_snake(item["id"]), item["description"], labels=["partition"]
            )

        for partition in partition_ids["items"]:
            data = fetch(
                self._api_host,
                self._api_session,
                f"/kpi/current/system/storageStats/partition/{partition['id']}",
            )
            for item in data["items"]:
                if not item["value"] is None:
                    metrics[item["id"]].add_metric(
                        labels=[partition["name"]], value=item["value"]
                    )

        for k, v in metrics.items():
            yield v
