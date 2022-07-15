"""
Prometheus collector for AudioCodes SBC v7.4.
"""
from argparse import ArgumentParser
from os import getenv
import time
from requests import Session
from requests.auth import HTTPBasicAuth
from prometheus_client import start_http_server

from audiocodes_exporter.collector import collect_sbc_metrics


def init_argparse() -> ArgumentParser:
    parser = ArgumentParser(
        description="Prometheus collector using AudioCodes SBC v7.4 API calls."
    )
    parser.add_argument(
        "-H",
        "--hostname",
        type=str,
        help="AudioCodes SBC API URL.",
        default=getenv("API_URL"),
        required=not getenv("API_URL"),
        dest="api_url",
    )
    parser.add_argument(
        "-u",
        "--username",
        type=str,
        help="Username to connect to the AudioCodes SBC API.",
        default=getenv("API_USERNAME"),
        required=not getenv("API_USERNAME"),
        dest="api_username",
    )
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        help="Password for the connecting user.",
        default=getenv("API_PASSWORD"),
        required=not getenv("API_PASSWORD"),
        dest="api_password",
    )

    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()

    session = Session()
    auth = HTTPBasicAuth(args.api_username, args.api_password)
    session.auth = auth

    collect_sbc_metrics(
        api_host=args.api_url,
        api_session=session,
    )
    print("starting server")
    start_http_server(9954)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
