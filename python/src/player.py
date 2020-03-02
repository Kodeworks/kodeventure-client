from core.model import PlayerModel
from log import Log
from quests.example import example_quest, example_websocket_quest


class Player(PlayerModel):
    """
    Implementation of the Player model
    """

    def __init__(self):
        """
        Construct a Kodeventure Player
        """

        super().__init__()

    def load_quests(self):
        """
        Register all your quest handlers here
        """

        # Add a quest handler for a regular HTTP POST request
        self.add_quest('POST', '/my-simple-quest', example_quest)

        # Add a quest handler for a quest request over websocket
        self.ws.quest_handlers.append(example_websocket_quest)

        Log.info('Quests loaded')
