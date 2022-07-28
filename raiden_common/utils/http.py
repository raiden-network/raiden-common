import re

from requests.adapters import HTTPAdapter

from raiden_common.utils.typing import Endpoint, Host, HostPort, Port


def split_endpoint(endpoint: Endpoint) -> HostPort:
    match = re.match(r"(?:[a-z0-9]*:?//)?([^:/]+)(?::(\d+))?", endpoint, re.I)
    if not match:
        raise ValueError("Invalid endpoint", endpoint)
    host, port = match.groups()
    if not port:
        port = "0"
    return Host(host), Port(int(port))


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = 0
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)
