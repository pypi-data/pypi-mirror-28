import json
from collections import namedtuple

import aiohttp

METHOD_GET = aiohttp.hdrs.METH_GET
METHOD_DELETE = aiohttp.hdrs.METH_DELETE
METHOD_POST = aiohttp.hdrs.METH_POST
METHOD_PUT = aiohttp.hdrs.METH_PUT
METHOD_PATCH = aiohttp.hdrs.METH_PATCH
CONTENT_TYPE = aiohttp.hdrs.CONTENT_TYPE
JSON_TYPE = 'application/json'

GET_METHODS = [METHOD_GET,
               METHOD_DELETE]

POST_METHODS = [METHOD_POST,
                METHOD_PUT,
                METHOD_PATCH]

ALL_METHODS = GET_METHODS + POST_METHODS

ALL_METHODS_LOWER = [method.lower() for method in ALL_METHODS]

__all__ = ['HttpClient',
           'HttpClientGroup',
           'METHOD_GET',
           'METHOD_DELETE',
           'METHOD_POST',
           'METHOD_PUT',
           'METHOD_PATCH']

ApiInfo = namedtuple('ApiInfo', ['url', 'headers'])
ApiResponse = namedtuple('ApiResponse', ['status', 'data'])


def format_path(path):
    return '{}'.format(path).strip('_')


async def format_response(response: aiohttp.ClientResponse, _json=json):
    content_type = response.headers.get(CONTENT_TYPE, '').lower()
    if JSON_TYPE not in content_type:
        return ApiResponse(response.status, await response.text())
    return ApiResponse(response.status, await response.json(loads=_json.loads))


class UrlBuilder:
    def __init__(self, http_client, url, headers, json_worker, *args):
        self.base_url = url
        self.headers = headers
        self.http_client = http_client
        self.sub_url = [format_path(arg) for arg in args]
        self.json = json_worker

    def __getattr__(self, item):
        self.sub_url.append(format_path(item))
        return self

    __getitem__ = __getattr__

    def __str__(self):
        return '{}/{}'.format(self.base_url,
                              "/".join(self.sub_url)) if self.sub_url else self.base_url

    __repr__ = __str__

    async def request(self, method, content=None, params=None, session=None, headers=None):
        if method not in ALL_METHODS:
            raise UnsupportedHttpMethod()
        if method in GET_METHODS and content:
            raise ContentInGet()
        return await self._check_session(method=method,
                                         url=self.__str__(),
                                         content=content,
                                         params=params,
                                         session=session,
                                         headers=headers)

    async def _check_session(self, headers=None, session=None, **kwargs):
        if not session:
            async with self.http_client.session(headers=headers) as session:
                return await self._make_request(session=session, **kwargs)
        return await self._make_request(session=session, **kwargs)

    async def _make_request(self, session, method, url, content=None, params=None):
        async with session.request(method, url, params=params, json=content) as response:
            return await format_response(response, self.json)

    async def get(self, params=None, **kwargs):
        return await self.request(method=METHOD_GET,
                                  params=params,
                                  **kwargs)

    async def delete(self, params=None, **kwargs):
        return await self.request(method=METHOD_DELETE,
                                  params=params,
                                  **kwargs)

    async def post(self, content=None, **kwargs):
        return await self.request(method=METHOD_POST,
                                  content=content,
                                  **kwargs)

    async def put(self, content=None, **kwargs):
        return await self.request(method=METHOD_PUT,
                                  content=content,
                                  **kwargs)

    async def patch(self, content=None, **kwargs):
        return await self.request(method=METHOD_PATCH,
                                  content=content,
                                  **kwargs)


class UnsupportedHttpMethod(Exception):
    pass


class ContentInGet(Exception):
    pass


class NoBaseUrl(Exception):
    pass


def session_maker(self, headers=None):
    headers = headers or {}
    if self.headers:
        headers.update(self.headers)
    return aiohttp.ClientSession(trust_env=True,
                                 headers=headers or None,
                                 json_serialize=self.json.dumps)


class HttpClient:
    def __init__(self, url, headers=None, json_worker=None):
        self.url = url
        self.headers = headers
        self.json = json_worker or json

    s = session = session_maker

    def __str__(self):
        return self.url

    def __getattr__(self, name):
        if name in ALL_METHODS_LOWER:
            return getattr(UrlBuilder(self, self.url, self.headers, self.json), name)
        return UrlBuilder(self, self.url, self.headers, self.json, name)

    __getitem__ = __getattr__


class HttpClientGroup:
    def __init__(self, *rules, json_worker=None):
        self.urls = {name: HttpClient(url, dict(headers), json_worker)
                     for name, url, *headers in rules}

    def __getattr__(self, name):
        if name in self.urls:
            return self.urls.get(name)
        else:
            raise NoBaseUrl('{} is not in urls'.format(name))
