from requests import Session

from prometheus_client import REGISTRY

from call_stats_collector import CallStatsCollector
from status_collector import StatusCollector


def collect_sbc_metrics(api_host: str, api_session: Session) -> None:
    print("registering status collector")
    REGISTRY.register(StatusCollector(api_host=api_host, api_session=api_session))
    print("registering call stats collector")
    REGISTRY.register(CallStatsCollector(api_host=api_host, api_session=api_session))
