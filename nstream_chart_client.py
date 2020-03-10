import asyncio
import os
import sys
from collections import deque

import asciichartpy

from nstream import NStream


def draw_screen(msg_buf, price_buf):
    print(chr(27) + "[2H" + chr(27) + "[2J")  # CLS
    if len(price_buf) > 1:
        print(asciichartpy.plot(list(price_buf), {"height": 25}))
    for msg in reversed(msg_buf):
        print(msg)


async def main(thing_id):
    price_buf = deque(maxlen=50)
    msg_buf = deque(maxlen=10)

    async def on_message(*, type, **kwargs):
        message = {"type": type, **kwargs}
        msg_buf.append(message)
        if type == "price":
            # TODO: this is very bogus, but we're only printing one chart so...
            price = (
                kwargs.get("ask")
                or kwargs.get("bid")
                or kwargs.get("bid1")
                or kwargs.get("ask1")
            )
            if price is not None:
                price_buf.append(price)
        draw_screen(msg_buf, price_buf)

    async with NStream(
        next_cookie=os.environ["NEXT_COOKIE"], on_message=on_message,
    ) as nstream:
        pump = await nstream.connect()
        await nstream.subscribe(thing_id)
        await pump


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]), debug=True)
