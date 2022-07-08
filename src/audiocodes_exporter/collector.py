from prometheus_client import REGISTRY
from requests import Session

from collectors.call_stats_collector import CallStatsCollector
from collectors.cluster_stats_collector import ClusterStatsCollector
from collectors.coder_stats_collector import CoderStatsCollector
from collectors.cpu_stats_collector import CpuStatsCollector
from collectors.ddos_stats_collector import DdosStatsCollector
from collectors.dsp_stats_collector import DspStatsCollector
from collectors.ha_stats_collector import HaStatsCollector
from collectors.license_stats_collector import LicenseStatsCollector
from collectors.media_stats_collector import MediaStatsCollector
from collectors.other_stats_collector import OtherStatsCollector
from collectors.port_stats_collector import PortStatsCollector
from collectors.siprec_stats_collector import SipRecStatsCollector
from collectors.status_collector import StatusCollector
from collectors.storage_stats_collector import StorageStatsCollector
from collectors.system_stats_collector import SystemStatsCollector
from helpers import fetch


def collect_sbc_metrics(api_host: str, api_session: Session) -> None:
    # Get the list of IP Groups with their ID, so we can use it to fetch specific metrics
    ip_group_data = fetch(
        api_host=api_host,
        api_session=api_session,
        api_endpoint="/kpi/current/sbc/callStats/ipGroup",
    )

    print("registering status collector")
    REGISTRY.register(StatusCollector(api_host, api_session))

    print("registering call stats collector")
    REGISTRY.register(CallStatsCollector(api_host, api_session, ip_group_data))

    print("registering other stats collector")
    REGISTRY.register(OtherStatsCollector(api_host, api_session, ip_group_data))

    print("registering SipRec stats collector")
    REGISTRY.register(SipRecStatsCollector(api_host, api_session, ip_group_data))

    print("registering cluster stats collector")
    REGISTRY.register(ClusterStatsCollector(api_host, api_session))

    print("registering coder stats collector")
    REGISTRY.register(CoderStatsCollector(api_host, api_session, ip_group_data))

    print("registering dsp stats collector")
    REGISTRY.register(DspStatsCollector(api_host, api_session))

    print("registering media stats collector")
    REGISTRY.register(MediaStatsCollector(api_host, api_session, ip_group_data))

    print("registering ddos stats collector")
    REGISTRY.register(DdosStatsCollector(api_host, api_session))

    print("registering ha stats collector")
    REGISTRY.register(HaStatsCollector(api_host, api_session))

    print("registering port stats collector")
    REGISTRY.register(PortStatsCollector(api_host, api_session))

    print("registering cpu stats collector")
    REGISTRY.register(CpuStatsCollector(api_host, api_session))

    print("registering license stats collector")
    REGISTRY.register(LicenseStatsCollector(api_host, api_session))

    print("registering storage stats collector")
    REGISTRY.register(StorageStatsCollector(api_host, api_session))

    print("registering system stats collector")
    REGISTRY.register(SystemStatsCollector(api_host, api_session))
