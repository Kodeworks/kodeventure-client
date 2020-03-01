import asyncio
from os import path
import ssl

from aiohttp import web, ClientSession

from config import PLAYER_HOST, PLAYER_PORT, PLAYER_TOKEN
from websocket import WebSocketHandler


class Player:
    headers = {
        'Authorization': PLAYER_TOKEN
    }

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.aiohttp = web.Application(
            loop=self.loop,
            middlewares=[],
        )
        self.client = ClientSession()
        self.ws = WebSocketHandler(self)
        self._ssl = self._load_ssl_certificates()

        self._config()

    def load_quests(self):
        # TODO: Add quests
        pass

    def connect(self):
        web.run_app(self.aiohttp, host=PLAYER_HOST, port=PLAYER_PORT, ssl_context=self._ssl)

    def _config(self):
        # Set up on_startup listener for connecting to the server
        self.aiohttp.on_startup.append(self.ws.connect)

        # Await websocket and client session termination
        async def _shutdown():
            await self.ws.close()
            await self.client.close()

        # Set up on_shutdown listeners for graceful shutdown
        self.aiohttp.on_shutdown.append(_shutdown)

    def _load_ssl_certificates(self) -> ssl.SSLContext:
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        sslcontext.load_cert_chain(
            path.join(path.dirname(__file__), '..', 'player.crt'),
            path.join(path.dirname(__file__), '..', 'player.key')
        )

        return sslcontext
