import asyncio
from os import path
import ssl

from colorama import Fore
from aiohttp import web, ClientSession

from config import PLAYER_HOST, PLAYER_PORT, PLAYER_TOKEN
from middleware import unhandled_route
from websocket import WebSocketHandler


class Player:
    headers = {
        'Authorization': PLAYER_TOKEN
    }

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.aiohttp = web.Application(
            loop=self.loop,
            middlewares=[unhandled_route],
        )
        self.client = ClientSession()
        self.ws = WebSocketHandler(self)
        self.cert = self._load_ssl_certificates()

        self.config()

    def load_quests(self):
        # TODO: Add quests
        pass

    def connect(self):
        web.run_app(
            self.aiohttp,
            host=PLAYER_HOST,
            port=PLAYER_PORT,
            ssl_context=self.cert
        )

    def config(self):
        # Set up on_startup listener for connecting to the server
        self.aiohttp.on_startup.append(self.ws.connect)

        # Await websocket and client session termination
        async def shutdown(app):
            await self.ws.close()
            await self.client.close()

        # Set up on_shutdown listeners for graceful shutdown
        self.aiohttp.on_shutdown.append(shutdown)

        # Add a default route
        self.aiohttp.router.add_route('*', '/', lambda request: web.json_response({ "msg": "I'm alive" }))

        # Load user defined quests
        self.load_quests()

    def _load_ssl_certificates(self) -> ssl.SSLContext:
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        sslcontext.load_cert_chain(
            path.join(path.dirname(__file__), '..', 'player.crt'),
            path.join(path.dirname(__file__), '..', 'player.key')
        )

        return sslcontext
