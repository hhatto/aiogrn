aiogrn
======

asyncio Groonga_ Client.

.. _Groonga: http://groonga.org/

Requirements
------------
* Python3.5+

Usage
-----

GQTP
~~~~

.. code-block:: python

    import asyncio
    from aiogrn.client import GroongaClient

    async def fetch(grn, cmd, **kwargs):
        ret = await grn.call(cmd, **kwargs)
        print(ret)

    loop = asyncio.get_event_loop()
    grn = GroongaClient(host='localhost', port=10043, protocol='gqtp', loop=loop)
    tasks = [
            asyncio.ensure_future(fetch(grn, 'status')),
            asyncio.ensure_future(fetch(grn, 'select', table='Foo')),
            asyncio.ensure_future(fetch(grn, 'status'))]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()


HTTP
~~~~

.. code-block:: python

    import asyncio
    from aiogrn.client import GroongaClient

    async def fetch(grn, cmd, **kwargs):
        ret = await grn.call(cmd, **kwargs)
        print(ret)

    loop = asyncio.get_event_loop()
    grn = GroongaClient(loop=loop)
    tasks = [
            asyncio.ensure_future(fetch(grn, 'status')),
            asyncio.ensure_future(fetch(grn, 'select', table='Foo')),
            asyncio.ensure_future(fetch(grn, 'status'))]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

