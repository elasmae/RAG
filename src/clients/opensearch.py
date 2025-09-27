from opensearchpy import OpenSearch
from ..settings import settings

_client = None

def get_client() -> OpenSearch:
    global _client
    if _client is None:
        _client = OpenSearch(
            hosts=[{"host": settings.os_host, "port": settings.os_port}],
            http_auth=(settings.os_user, settings.os_password),
            use_ssl=settings.os_use_ssl,
            verify_certs=False,
        )
    return _client
