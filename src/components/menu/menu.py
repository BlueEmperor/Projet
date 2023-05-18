import pygame
from sys import exit

from src.components.menu.button import Button
from src.config import Config
from src.services.visualization_service import VisualizationService
from src.global_state import GlobalState
from src.components.status import GameStatus

vec = pygame.math.Vector2

class Menu:
    def __init__(self):
        self.background = VisualizationService.get_background_image()
        self.buttons = [
            Button(vec(Config.WIDTH/2-300/2, 150),vec(300,100), (245, 161, 38), "Play", self.play),
            Button(vec(Config.WIDTH/2-300/2, 300),vec(300,100), (245, 161, 38), "Exit", self.exit)
        ]
    
    def draw(self, SCREEN):
        SCREEN.blit(self.background, (0,0))
        for button in self.buttons:
            button.draw(SCREEN)

    def click_event(self):
        for button in self.buttons:
            if(button.rect.collidepoint(pygame.mouse.get_pos())):
                button.function()
                return
                
    def play(self):
        GlobalState.GAME_STATE = GameStatus.GAMEPLAY
    
    def exit(self):
        pygame.quit()
        exit()