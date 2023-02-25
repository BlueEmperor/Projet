import pygame

from src.components.items.basic_sword import BasicSword
from src.components.items.basic_bow import BasicBow
from src.components.items.epic_sword import EpicSword
from src.global_state import GlobalState
from src.components.status import PlayerStatus
from src.config import Config

vec = pygame.math.Vector2

class Inventory:
    def __init__(self):
        self.size=16
        self.items=[]
        self.in_hotbar=[BasicSword(),EpicSword(),BasicBow()]
        self.is_open=False
        self.offset=0
        self.WIDTH = 250
        self.HEIGHT = Config.HEIGHT-50
        self.speed=5
        self.offset = -self.WIDTH
        self.col = 4

    def draw(self, SCREEN):
        self.rect=pygame.Rect(self.offset,25,self.WIDTH,self.HEIGHT)
        pygame.draw.rect(SCREEN, (84, 84, 84), self.rect)
        if(self.is_open):
            if(self.offset<25):
                self.offset+=self.speed
        else:
            if(self.offset>-self.WIDTH):
                self.offset-=self.speed
        
        #SCREEN.blit(self.entity_save.image,vec(self.x+self.offset+30,30))
        #SCREEN.blit(self.font.render(str(self.entity_save.health),True,(255, 255, 255)), vec(self.x+self.offset+100,40))
        


    def events_handle(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pass
            elif(event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                if(self.is_open):
                    self.is_open=False
                    GlobalState.PLAYER_STATE = PlayerStatus.MOVEMENT
                else:
                    self.is_open=True
                    GlobalState.PLAYER_STATE = PlayerStatus.INVENTORY_MENU
        
        for item in self.items:
            if(item.rect.collidepoint(pygame.mouse.get_pos())):
                pass