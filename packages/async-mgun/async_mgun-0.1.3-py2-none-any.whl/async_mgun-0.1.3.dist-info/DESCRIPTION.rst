==========
async-mgun
==========

.. image:: https://badge.fury.io/py/async-mgun.svg
    :target: https://pypi.python.org/pypi/async-mgun
.. image:: https://travis-ci.org/maximdanilchenko/async-mgun.svg
    :target: https://travis-ci.org/maximdanilchenko/async-mgun
.. image:: https://codecov.io/gh/maximdanilchenko/async-mgun/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/maximdanilchenko/async-mgun

HTTP REST Client based on aiohttp with dynamic url building. Useful for microservices non-blocking communication

Quickstart
----------

.. code-block:: python


    from mgun import HttpClient
    import asyncio

    client = HttpClient('https://httpbin.org')


    async def request():
        resp = await client.anything.api.users[23].address.get({'q': '12'})

        print(resp.status)  # 200
        print(resp.data['url'])  # https://httpbin.org/anything/api/users/23/address?q=12

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([request()]))




