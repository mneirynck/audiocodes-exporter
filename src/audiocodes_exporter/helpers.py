import re
from typing import Any
from requests import Session


def fetch(api_host: str, api_session: Session, api_endpoint: str) -> dict[str, Any]:
    """
    Get metrics from AudioCodes SBC API and refresh Prometheus metrics with new values
    """

    # Fetch raw status data from the application
    response = api_session.get(url=f"{api_host}/api/v1{api_endpoint}")
    data = response.json()
    return data


def convert(obj) -> Any:
    if isinstance(obj, bool):
        return str(obj).lower()
    if isinstance(obj, int):
        return str(obj).lower()
    if isinstance(obj, (list, tuple)):
        return [convert(item) for item in obj]
    if isinstance(obj, dict):
        return {convert(key): convert(value) for key, value in obj.items()}
    return obj


def camel_to_snake(string) -> str:
    groups = re.findall("([A-z0-9][a-z]*)", string)
    return "_".join([i.lower() for i in groups])
