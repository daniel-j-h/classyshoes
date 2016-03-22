from time import sleep
from urllib.parse import urljoin
from requests import Session


# Constructs an endpoint as: site ++ /path
def mkEndpoint(base, path):
    return urljoin(base, path)


# JSON from HTTP request, throws on error (status codes 4XX and 5XX)
def mkJSON(session, endpoint, headers, params):
    response = session.get(endpoint, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


# Scoped session with HTTP Keep-Alive property
def mkKeepAliveSession():
    return Session()


# Generator for lazily walking paginated endpoint
def mkIterable(session, endpoint, headers, fields, progress, timeout, pageSize=100):
    params = {'page': 1, 'pageSize': pageSize, 'fields': fields}
    firstPage = mkJSON(session, endpoint, headers, params)
    yield from firstPage['content']

    totalPages = int(firstPage['totalPages'])

    # Pages are 1-indexed, and got first already
    for pageId in progress(range(2, totalPages + 1)):
        sleep(timeout)

        params = {'page': pageId, 'pageSize': pageSize, 'fields': fields}
        yield from mkJSON(session, endpoint, headers, params)['content']
