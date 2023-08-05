import json
from http import client
from urllib.parse import urlparse

URL_FORMAT = "{server}/badge/{user}/{repo}/{subject}"
SVG_URL_FORMAT = "{server}/badge/{user}/{repo}/{subject}.svg"

def upload(server: str, user: str, repo: str, subject: str, status: str, color: str) -> None:
    url = URL_FORMAT.format(server=server, user=user, repo=repo, subject=subject)
    parts = urlparse(url)
    connection = client.HTTPConnection(host=parts.hostname, port=parts.port)
    headers = {"Content-Type": "application/json"}
    connection.request('PUT', parts.path,
        body=json.dumps(dict(status=status, color=color)), headers=headers)
    response = connection.getresponse()
    response.read()

    return SVG_URL_FORMAT.format(
        server=server, user=user, repo=repo, subject=subject)
