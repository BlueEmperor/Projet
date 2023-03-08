import pygame

from src.components.status import GameStatus, PlayerStatus
from src.config import Config


class GlobalState:
    GAME_STATE = GameStatus.MAIN_MENU
    PLAYER_STATE = PlayerStatus.MOVEMENT
    SCREEN = None

    @staticmethod
    def load_main_screen():
        screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        screen.fill((0, 0, 0))
        GlobalState.SCREEN = screen
        
