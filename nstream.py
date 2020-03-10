import asyncio

import aiohttp
from aiohttp import WSMsgType


class NStream:
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"

    def __init__(self, *, next_cookie, on_message):
        self.next_cookie = next_cookie
        self.ready_event = asyncio.Event()
        self.client_session = aiohttp.ClientSession()
        self.sock = None
        self.on_message = on_message

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.sock:
            await self.sock.close()
            self.sock = None
        await self.client_session.close()

    async def connect(self):
        self.sock = await self.client_session.ws_connect(
            "wss://www.nordnet.fi/ws/2/public",
            origin="https://www.nordnet.fi",
            protocols=["NEXT"],
            headers={
                "Cookie": ("NEXT=%s" % self.next_cookie),
                "User-Agent": self.USER_AGENT,
            },
            autoclose=False,
        )
        return asyncio.create_task(self.pump())

    async def subscribe(self, thing_id):
        thing_id = int(thing_id)
        await self.ready_event.wait()
        await self.sock.send_json(
            {"cmd": "subscribe", "args": {"t": "price", "id": thing_id}}
        )
        await self.sock.send_json(
            {"cmd": "subscribe", "args": {"t": "depth", "id": thing_id}}
        )
        await self.sock.send_json(
            {"cmd": "subscribe", "args": {"t": "trade", "id": thing_id}}
        )

    async def pump(self):
        while self.sock:
            msg = await self.sock.receive()
            if msg.type == WSMsgType.CLOSED:
                break
            if msg.type == WSMsgType.TEXT:
                data = msg.json()
                data_type = data.get("type")
                data_data = data.get("data", {})
                if data_type == "ack":
                    if data_data.get("cmd") == "login":
                        self.ready_event.set()
                await self.on_message(type=data_type, **data_data)
