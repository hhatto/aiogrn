import asyncio
from aiogrn.client import GroongaClient


async def fetch(grn, cmd, **kwargs):
    ret = await grn.call(cmd, **kwargs)
    print(ret)


def main():
    loop = asyncio.get_event_loop()
    grn = GroongaClient(host='127.0.0.1', port=10043, protocol='gqtp', loop=loop)
    tasks = [
            asyncio.ensure_future(fetch(grn, 'status')),
            asyncio.ensure_future(fetch(grn, 'select', table='Foo')),
            asyncio.ensure_future(fetch(grn, 'status'))]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

if __name__ == '__main__':
    main()
