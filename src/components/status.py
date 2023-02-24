from enum import Enum

class GameStatus(Enum):
    MAIN_MENU = 0
    GAMEPLAY = 1
    GAME_END = 2

class PlayerStatus(Enum):
    MOVEMENT = 0
    ATTACK = 1
    PAUSE_MENU = 2
    INVENTORY_MENU = 3