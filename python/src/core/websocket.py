import json

from aiohttp import ClientSession
from aiohttp import WSMsgType

from config import SERVER_HOST
from log import Log


# The websocket endpoint of the server
WS_URI: str = f'https://{SERVER_HOST}/ws'

# The different game messages that can be received
GAME_MESSAGES = (
    'game_started',
    'game_message',
    'game_paused',
    'game_unpaused',
    'game_ended'
)


class WebSocketHandler:
    """
    The websocket handler wraps the connection and parsing of messages from the server.
    It also keeps a reference to the socket so other components can send messages to the server.
    """

    def __init__(self, player):
        """
        Construct a new websocket handler
        :param player: The Player object to connect with
        """

        self.player = player
        self.quest_handlers = []
        self.socket = None

    async def connect(self, *args):
        """
        Connect to the Kodeventure server
        :param args: Positional args
        """

        try:
            self.socket = await self.player.client.ws_connect(
                WS_URI,
                headers=self.player.headers,
                ssl=False
            )

            Log.info(f'[WS] Connected to {WS_URI}')

            self.player.aiohttp.loop.create_task(self.run())
        except Exception as e:
            Log.error(f'[WS] Failed to connect to ${WS_URI}: {e}')

    async def run(self):
        """
        Start asynchronously reading messages from the server
        """

        try:
            async for msg in self.socket:
                if msg.type == WSMsgType.ERROR:
                    self.handle_error(msg)
                    break
                elif msg.type == WSMsgType.TEXT:
                    await self.handle_message(msg.data)
                elif msg.type == WSMsgType.CLOSING:
                    self.handle_closing(msg)
        finally:
            Log.info(f'[WS] Connection to server was closed')

    async def send(self, data):
        """
        Send some JSON data over the socket.
        :param data: A Python dictionary with the data to send.
        """

        if not isinstance(data, dict):
            Log.error(f'Could not send {data} to server, as it is not a dictionary')

        if self.socket is not None:
            await self.socket.send_json(data)
        else:
            Log.error(f'Could not send {data} to server, as there is no active websocket')

    async def close(self):
        """
        Close the current connection to the server, if it is active
        """

        if self.socket is not None:
            await self.socket.close()

    async def handle_message(self, msg: str):
        """
        Event handler for regular text messages received from the server.
        :param msg: The message body as text
        """

        payload = json.loads(msg)
        event_type = payload['type']
        data = payload['data']

        # Handle regular game messages
        if event_type in GAME_MESSAGES:
            Log.server(event_type, data["msg"])
        # Handle a quest request
        elif event_type == 'player_quest_request':
            for handler in self.quest_handlers:
                await handler(data, self.player)
        # Handle game errors related to this player
        elif event_type == 'player_error':
            Log.error(f'[SERVER] (player_error) {data}')
        # Handle all other messages
        else:
            Log.error(f'[SERVER] ({event_type}) {data}')

    def handle_error(self, msg: str):
        """
        Event handler for errors occurring from the websocket object
        :param msg: The message body as text
        """

        Log.error(f'[WS] {msg}')

    def handle_closing(self, msg):
        """
        Event handler for when the server signals it is closing
        :param msg: The message body as text
        """

        Log.info(f'[WS] Connection to server is closing: {msg}')
