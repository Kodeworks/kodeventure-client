from core.model import PlayerModel
from log import Log
from quests.example import example_quest


class Player(PlayerModel):
    """
    Implementation of the Player model
    """

    def __init__(self):
        """
        Construct a Kodeventure Player
        """

        super().__init__(self)

    def load_quests(self):
        """
        Register all your quest handlers here
        """

        Log.info('Quests loaded')
