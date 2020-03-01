from os import path

import colorama

from cert import init_certificate
from player import Player

colorama.init(autoreset=True)


if __name__ == '__main__':
    init_certificate()

    player = Player()
    player.connect()
