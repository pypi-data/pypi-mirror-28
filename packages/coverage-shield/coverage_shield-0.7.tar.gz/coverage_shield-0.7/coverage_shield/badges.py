import json
from http import client
from urllib.parse import urlparse

URL_FORMAT = "{server}/badge/{user}/{repo}/{subject}"
SVG_URL_FORMAT = "{server}/badge/{user}/{repo}/{subject}.svg"

def _put(url, headers, body, redirects=5):
    parts = urlparse(url)
    ctr = client.HTTPSConnection if parts.scheme == 'https' else client.HTTPConnection
    connection = ctr(host=parts.hostname, port=parts.port)
    connection.request(
        'PUT', parts.path,
        body=body, headers=headers)
    response = connection.getresponse()
    if response.status in (301, 302, 307, 308):
        if redirects == 0:
            raise client.HTTPException("Too many redirects")
        _put(response.headers.get('location'), headers, body, redirects=redirects-1)
    return response

def upload(server: str, user: str, repo: str, subject: str, status: str, color: str) -> None:
    url = URL_FORMAT.format(server=server, user=user, repo=repo, subject=subject)
    r = _put(url,
             headers={"Content-Type": "application/json"},
             body=json.dumps(dict(status=status, color=color)))
    if r.status >= 200 and r.status < 300:
        return SVG_URL_FORMAT.format(
            server=server, user=user, repo=repo, subject=subject)

    raise client.HTTPException("HTTP Error: {}".format(r.status))
