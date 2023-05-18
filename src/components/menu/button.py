import pygame

from src.services.visualization_service import VisualizationService

vec = pygame.math.Vector2

class Button:
    def __init__(self, coord : tuple, size : tuple, color : tuple, text : str, function) -> None:
        self.coord = coord
        self.size = size
        self.color = color
        self.text = text
        self.font = VisualizationService.get_main_font()
        self.rect = pygame.Rect(self.coord,self.size)
        self.function = function

    def draw(self, SCREEN) -> None:
        if(self.rect.collidepoint(pygame.mouse.get_pos())):
            pygame.draw.rect(SCREEN, (255,255,255), self.rect)
        else:
            pygame.draw.rect(SCREEN, self.color, self.rect)
        text=VisualizationService.get_main_font().render(self.text,True,(0,0,0))
        text_rect=text.get_rect()
        SCREEN.blit(text, self.coord+self.size*0.5-vec(text_rect[2]/2,text_rect[3]/2))