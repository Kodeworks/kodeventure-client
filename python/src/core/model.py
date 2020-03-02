from abc import abstractmethod, ABC
import asyncio
from os import path
import ssl

from colorama import Fore
from aiohttp import web, ClientSession

from config import PLAYER_HOST, PLAYER_PORT, PLAYER_TOKEN, SERVER_HOST
from core.middleware import unhandled_route
from core.websocket import WebSocketHandler
from log import Log


class PlayerModel(ABC):
    """
    Base Player class responsible for maintaining all state and connect to the Kodeventure server
    """

    headers = {
        'Authorization': PLAYER_TOKEN
    }

    def __init__(self):
        """
        Construct a new Player
        """

        self.loop = asyncio.get_event_loop()
        self.aiohttp = web.Application(
            loop=self.loop,
            middlewares=[unhandled_route],
        )
        self.client = ClientSession()
        self.ws = WebSocketHandler(self)
        self.cert = self._load_ssl_certificates()

        self.config()

    @abstractmethod
    def load_quests(self):
        """
        Load all quest handlers here
        """

        raise NotImplementedError()

    def add_quest(self, method: str, route: str, handler):
        """
        Add a quest handler to the aiohttp app
        :param method: The HTTP method to handle, i.e GET, POST, PUT, DELETE, HEAD, OPTIONS
        :param route: The route to add
        :param handler: The request handler function that will process the request
        """

        self.aiohttp.router.add_route(method, route, handler)

    def connect(self):
        """
        Start the application and connect to the server
        """

        Log.info(f'Connecting to Kodeventure server at {SERVER_HOST}')
        web.run_app(
            self.aiohttp,
            host=PLAYER_HOST,
            port=PLAYER_PORT,
            ssl_context=self.cert
        )

    def config(self):
        """
        Configure the Player object by attaching some event handlers, adding default route and loading quests
        """

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
        """
        Private helper to load SSL certificates from disk
        """

        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        sslcontext.load_cert_chain(
            path.join(path.dirname(__file__), '..', 'player.crt'),
            path.join(path.dirname(__file__), '..', 'player.key')
        )

        return sslcontext
