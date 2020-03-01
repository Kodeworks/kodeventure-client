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
        self.socket = await self.player.client.ws_connect(
            WS_URI,
            headers=self.player.headers,
            ssl=False
        )

        async for msg in self.socket:
            if msg.type == WSMsgType.ERROR:
                self.handle_error
                break
            elif msg.type == WSMsgType.TEXT:
                self.handle_message(msg.data)

        return self.socket

    async def close(self, *args):
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
