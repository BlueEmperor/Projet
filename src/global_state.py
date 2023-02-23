import pygame

from src.components.game_status import GameStatus
from src.config import Config


class GlobalState:
    GAME_STATE = GameStatus.GAMEPLAY
    PLAYER_STATE = 
    SCREEN = None

    @staticmethod
    def load_main_screen():
        screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        screen.fill((0, 0, 0))
        GlobalState.SCREEN = screen
