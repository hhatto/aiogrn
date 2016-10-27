import struct
import sys
import asyncio
import aiohttp
import async_timeout
from urllib.parse import urlencode
from poyonga.const import GQTP_HEADER_SIZE
from poyonga.client import Groonga, get_send_data_for_gqtp, convert_gqtp_result_data
from poyonga.result import GroongaSelectResult, GroongaResult


class GroongaClient(object):

    def __init__(self, host='localhost', port=10041, protocol='http', encoding='utf-8',
                 prefix_path='/d/', loop=None):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.encoding = encoding
        self.prefix_path = prefix_path
        self._recv_buf = 8192
        self._timeout = 3
        self._grn = Groonga()
        self.loop = loop or asyncio.get_event_loop()

    async def _http_fetch(self, session, url):
        with async_timeout.timeout(self._timeout):
            async with session.get(url) as resp:
                return await resp.text()

    async def _call_http(self, cmd, **kwargs):
        domain = [self.protocol, "://", self.host, ":", str(self.port), self.prefix_path]
        url = "".join(domain) + cmd
        if kwargs:
            url = "".join([url, "?", urlencode(kwargs)])
        async with aiohttp.ClientSession(loop=self.loop) as session:
            return await self._http_fetch(session, url)

    async def _call_gqtp(self, cmd, **kwargs):
        _start = self._grn._clock_gettime()
        with async_timeout.timeout(self._timeout):
            _r, _w = await asyncio.open_connection(self.host, self.port, loop=self.loop)
        _w.write(get_send_data_for_gqtp(cmd, **kwargs))
        with async_timeout.timeout(self._timeout):
            await _w.drain()
        with async_timeout.timeout(self._timeout):
            raw_data = await _r.read(self._recv_buf)
        proto, qtype, keylen, level, flags, status, size, opaque, cas \
            = struct.unpack("!BBHBBHIIQ", raw_data[:GQTP_HEADER_SIZE])
        while len(raw_data) < size + GQTP_HEADER_SIZE:
            raw_data += await _r.read(self._recv_buf)
        _end = self._grn._clock_gettime()
        _w.close()
        return convert_gqtp_result_data(_start, _end, status, raw_data)

    async def call(self, cmd, **kwargs):
        output_type = kwargs.get("output_type") or 'json'
        if self.protocol == 'http':
            result = await self._call_http(cmd, **kwargs)
        else:
            result = await self._call_gqtp(cmd, **kwargs)
        if cmd == 'select':
            return GroongaSelectResult(result, output_type, self.encoding)
        return GroongaResult(result, output_type, self.encoding)
