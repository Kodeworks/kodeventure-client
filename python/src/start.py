from os import path

from core.cert import init_certificate
from log import Log
from player import Player


if __name__ == '__main__':
    init_certificate()

    player = Player()
    player.connect()
