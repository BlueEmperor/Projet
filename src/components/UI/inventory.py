import pygame

from src.components.items.basic_sword import BasicSword
from src.components.items.basic_bow import BasicBow
from src.components.items.epic_sword import EpicSword
from src.global_state import GlobalState
from src.components.status import PlayerStatus
from src.config import Config
from src.services.visualization_service import VisualizationService

vec = pygame.math.Vector2

class Inventory:
    def __init__(self):
        self.size=16
        self.items=[BasicSword(),EpicSword(),BasicBow(),BasicSword(),EpicSword(),BasicBow(),BasicSword(),EpicSword(),BasicBow(),BasicSword(),EpicSword(),BasicBow()]
        self.in_hotbar=[BasicSword(),EpicSword(),BasicBow()]
        self.is_open=False
        self.offset=0
        self.WIDTH = 320
        self.HEIGHT = Config.HEIGHT-50
        self.speed=5
        self.offset = -self.WIDTH
        self.col = 4
        self.rect=pygame.Rect(self.offset,25,self.WIDTH,self.HEIGHT)
        self.alpha_screen = pygame.Surface((Config.WIDTH, Config.HEIGHT), pygame.SRCALPHA)
        self.item_on_cursor = None
        self.font=VisualizationService.get_main_font()
        self.alpha=200

    def draw(self, SCREEN, player):

        if(self.is_open):
            if(self.offset<25):
                self.offset+=self.speed
        else:
            if(self.offset>-self.WIDTH):
                self.offset-=self.speed
        
        self.alpha_screen.fill((0,0,0,0))
        self.rect=pygame.Rect(self.offset,25,self.WIDTH,self.HEIGHT)
        pygame.draw.rect(self.alpha_screen, (84,84,84, self.alpha), self.rect)
        self.alpha_screen.blit(self.font.render("Inventaire",True,(255, 255, 255)), (self.offset+125,50))
        self.alpha_screen.blit(player.image, vec(self.offset+25,50))

        for i in range(self.col):
            for j in range(int(self.size//self.col)):
                pygame.draw.rect(self.alpha_screen, (51, 51, 51, self.alpha), pygame.Rect(j*70+25+self.offset,120+i*70, 64, 64))
                if(len(self.items)>i*4+j):
                    self.items[i*4+j].rect.topleft=vec(j*70+25+self.offset,120+i*70)
                    self.alpha_screen.blit(self.items[i*4+j].image,vec(self.offset+j*70+25,120+i*70))

        SCREEN.blit(self.alpha_screen, (0,0))

        if(self.item_on_cursor!=None):
            rect=pygame.Rect(0,0,200,100)
            rect.bottomleft=pygame.mouse.get_pos()
            pygame.draw.rect(SCREEN, (30, 30, 30, self.alpha), rect)
            SCREEN.blit(self.font.render("Damage : " + str(self.item_on_cursor.damage),True,(255, 255, 255)), (rect.topleft[0]+10,rect.topleft[1]+10))
            SCREEN.blit(self.font.render("Portée : " + str(self.item_on_cursor.range),True,(255, 255, 255)), (rect.topleft[0]+10,rect.topleft[1]+40))

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
                self.item_on_cursor=item
                return
        
        self.item_on_cursor=None