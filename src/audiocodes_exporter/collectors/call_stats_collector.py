"""
Prometheus collectors for AudioCodes SBC.
"""
from typing import Any

from prometheus_client.core import GaugeMetricFamily
from requests import Session

from audiocodes_exporter.helpers import camel_to_snake, fetch


class CallStatsCollector:
    """
    Collects AudioCodes SBC call statistics from the API endpoint
    """

    def __init__(
        self, api_host: str, api_session: Session, ip_group_data: dict[str, Any]
    ) -> None:
        self._api_host = api_host
        self._api_session = api_session
        self._ip_group_data = ip_group_data

    def collect(self):
        """
        api response:
        {
           "items":[
              {
                 "id":"abnormalTerminatedCallsInTotal",
                 "name":"Abnormal Terminated Calls In Total",
                 "description":"Total number of abnormally terminated inbound calls (after connect)",
                 "url":"/api/v1/kpi/current/sbc/callStats/global/abnormalTerminatedCallsInTotal",
                 "value":76
              },
            ...
        """

        global_data = fetch(
            api_host=self._api_host,
            api_session=self._api_session,
            api_endpoint="/kpi/current/sbc/callStats/global",
        )

        metrics = {}

        for item in global_data["items"]:
            metrics[item["id"]] = GaugeMetricFamily(
                camel_to_snake(item["id"]), item["description"], labels=["entity"]
            )

            if not item["value"] is None:
                metric_id = item["id"]

                metrics[metric_id].add_metric(labels=["global"], value=item["value"])

        # Get the list of IP Groups with their ID, so we can use it to fetch specific metrics
        for ip_group in self._ip_group_data["items"]:
            ip_group_name = ip_group["name"]
            data = fetch(
                api_host=self._api_host,
                api_session=self._api_session,
                api_endpoint=f"/kpi/current/sbc/callStats/ipGroup/{ip_group['id']}",
            )
            for item in data["items"]:
                if not item["value"] is None:
                    metrics[item["id"]].add_metric(
                        labels=[ip_group_name], value=item["value"]
                    )

        for k, v in metrics.items():
            yield v
