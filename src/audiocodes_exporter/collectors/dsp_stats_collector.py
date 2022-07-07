"""
Prometheus collectors for AudioCodes SBC.
"""
from typing import Any

from prometheus_client.core import GaugeMetricFamily
from requests import Session

from helpers import camel_to_snake, fetch


class DspStatsCollector:
    """
    Collects AudioCodes SBC DSP statistics from the API endpoint
    """

    def __init__(self, api_host: str, api_session: Session) -> None:
        self._api_host = api_host
        self._api_session = api_session

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
            api_endpoint="/kpi/current/media/dspStats/global",
        )

        metrics = {}

        for item in global_data["items"]:
            metrics[item["id"]] = GaugeMetricFamily(
                camel_to_snake(item["id"]), item["description"], labels=["entity"]
            )

            if not item["value"] is None:
                metric_id = item["id"]

                metrics[metric_id].add_metric(labels=["global"], value=item["value"])

        for k, v in metrics.items():
            yield v
