import pygame

from src.config import Config
from src.services.visualization_service import VisualizationService

vec = pygame.math.Vector2

class DisplayInfo:
    def __init__(self):
        self.font=VisualizationService.get_main_font()
        self.entity = None
        self.entity_save = None
        self.WIDTH = 224
        self.HEIGHT = 100
        self.speed=8
        self.offset = self.WIDTH
        self.x=Config.WIDTH-self.WIDTH
        
    def draw(self, SCREEN):
        self.rect=pygame.Rect(self.x+self.offset,0,self.WIDTH,self.HEIGHT)
        pygame.draw.rect(SCREEN, (84, 84, 84), self.rect)
        if(self.entity == None):
            if(self.offset<self.WIDTH):
                self.offset+=8
            else:
                self.entity_save = None
        else:
            if(self.offset>0):
                self.offset-=8
        
        if(self.entity_save!=None):
            SCREEN.blit(self.entity_save.image,vec(self.x+self.offset+30,30))
            SCREEN.blit(self.font.render(str(self.entity_save.health),True,(255, 255, 255)), vec(self.x+self.offset+100,40))
        
