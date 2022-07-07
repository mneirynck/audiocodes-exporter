"""
Prometheus collectors for AudioCodes SBC.
"""
from prometheus_client.core import GaugeMetricFamily
from requests import Session

from helpers import convert, fetch


class StatusCollector:
    """
    Collects AudioCodes SBC Status info
    """

    def __init__(self, api_host: str, api_session: Session) -> None:
        self._api_host = api_host
        self._api_session = api_session

    def collect(self):
        """
        api response:
        {
            "localTimeStamp":"2022-07-06T21:36:39+01:00",
            "ipAddress":"10.101.95.174",
            "subnetMask":"255.255.224.0",
            "defaultGateway":"10.101.64.1",
            "productType":"Mediant VE SBC",
            "versionID":"7.40A.100.838",
            "protocolType":"SIP",
            "operationalState":"UNLOCKED",
            "highAvailability":"Operational",
            "serialNumber":"98517064501590",
            "macAddress":"020a17bdb526",
            "osType":"8",
            "acceleratedNetworking":"enabled",
            "systemUpTime":13420550,
            "saveNeeded":false,
            "resetNeeded":false
        }
        """
        # print(self._api_data)
        api_data = fetch(
            api_host=self._api_host,
            api_session=self._api_session,
            api_endpoint="/status",
        )

        status = {key: value for key, value in api_data.items()}

        labels, label_values = zip(*convert(status).items())

        status_metric = GaugeMetricFamily(
            "sbc_status_info", "AudioCodes SBC status info.", labels=labels
        )
        status_metric.add_metric(label_values, 1)

        yield status_metric
