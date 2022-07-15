"""
Prometheus collectors for AudioCodes SBC.
"""

from typing import Any
from prometheus_client.core import GaugeMetricFamily
from requests import Session

from audiocodes_exporter.helpers import camel_to_snake, fetch


class SipRecStatsCollector:
    """
    Collects AudioCodes SBC SIPRec statistics from the API endpoint
    """

    def __init__(
        self, api_host: str, api_session: Session, ip_group_data: dict[str, Any]
    ) -> None:
        self._api_host = api_host
        self._api_session = api_session
        self._ip_group_data = ip_group_data

    def collect(self):
        global_data = fetch(
            api_host=self._api_host,
            api_session=self._api_session,
            api_endpoint="/kpi/current/sbc/sipRecstats/global",
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

        for ip_group in self._ip_group_data["items"]:
            ip_group_name = ip_group["name"]
            data = fetch(
                api_host=self._api_host,
                api_session=self._api_session,
                api_endpoint=f"/kpi/current/sbc/sipRecstats/ipGroup/{ip_group['id']}",
            )
            for item in data["items"]:
                if not item["value"] is None:
                    metrics[item["id"]].add_metric(
                        labels=[ip_group_name], value=item["value"]
                    )

        for k, v in metrics.items():
            yield v
