import pygame

from src.components.menu.button import Button
from src.config import Config
from src.services.visualization_service import VisualizationService

vec = pygame.math.Vector2

class Menu:
    def __init__(self):
        self.background = VisualizationService.get_background_image()
        self.buttons = [
            Button(vec(Config.WIDTH/2-300/2, Config.HEIGHT/2-150/2),vec(50,20), (245, 161, 38), "test")
        ]
    
    def draw(self, SCREEN):
        SCREEN.blit(self.background, (0,0))
        for button in self.buttons:
            button.draw(SCREEN)
