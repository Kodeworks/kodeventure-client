import json

from aiohttp import ClientSession
from aiohttp import WSMsgType
from colorama import Fore

from config import SERVER_HOST


WS_URI: str = f'https://{SERVER_HOST}/ws'

GAME_MESSAGES = (
    'game_started',
    'game_message',
    'game_paused',
    'game_unpaused',
    'game_ended'
)


class WebSocketHandler:
    def __init__(self, player):
        self.player = player
        self.socket = None

    async def connect(self, *args):
        try:
            self.socket = await self.player.client.ws_connect(
                WS_URI,
                headers=self.player.headers,
                ssl=False
            )

            print(f'Connected to {WS_URI}')
            self.player.aiohttp.loop.create_task(self.run())
        except Exception as e:
            print(f'{Fore.RED}[WS] Failed to connect to ${WS_URI}: {e}')



    async def run(self):
        try:
            async for msg in self.socket:
                if msg.type == WSMsgType.ERROR:
                    self.handle_error(msg)
                    break
                elif msg.type == WSMsgType.TEXT:
                    self.handle_message(msg.data)
                elif msg.type == WSMsgType.CLOSING:
                    self.handle_closing(msg)
        finally:
            print(f'[WS] Connection to server was closed')

    async def close(self):
        if self.socket is not None:
            await self.socket.close()

    def handle_message(self, msg):
        payload = json.loads(msg)
        event_type = payload['type']
        data = payload['data']

        if event_type in GAME_MESSAGES:
            print(f'{Fore.CYAN}[SERVER] ({event_type}) {data["msg"]}')
        elif event_type == 'player_error':
            print(f'{Fore.RED}[SERVER] ({event_type}) {data}')
        else:
            print(f'{Fore.RED}[SERVER] ({event_type}) {data}')

    def handle_error(self, msg):
        print(f'{Fore.RED}[WS] Error: {msg}')

    def handle_closing(self, msg):
        print(f'[WS] Connection to server is closing: {msg}')
