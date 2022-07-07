from prometheus_client import REGISTRY
from requests import Session

from call_stats_collector import CallStatsCollector
from helpers import fetch
from other_stats_collector import OtherStatsCollector
from status_collector import StatusCollector


def collect_sbc_metrics(api_host: str, api_session: Session) -> None:
    # Get the list of IP Groups with their ID, so we can use it to fetch specific metrics
    ip_group_data = fetch(
        api_host=api_host,
        api_session=api_session,
        api_endpoint="/kpi/current/sbc/callStats/ipGroup",
    )

    print("registering status collector")
    REGISTRY.register(StatusCollector(api_host=api_host, api_session=api_session))

    print("registering call stats collector")
    REGISTRY.register(
        CallStatsCollector(
            api_host=api_host, api_session=api_session, ip_group_data=ip_group_data
        )
    )

    print("registering other stats collector")
    REGISTRY.register(
        OtherStatsCollector(
            api_host=api_host, api_session=api_session, ip_group_data=ip_group_data
        )
    )
