from prometheus_client import REGISTRY
from requests import Session

from collectors.call_stats_collector import CallStatsCollector
from collectors.other_stats_collector import OtherStatsCollector
from collectors.siprec_stats_collector import SipRecStatsCollector
from collectors.status_collector import StatusCollector
from helpers import fetch


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

    print("registering SipRec stats collector")
    REGISTRY.register(
        SipRecStatsCollector(
            api_host=api_host, api_session=api_session, ip_group_data=ip_group_data
        )
    )
