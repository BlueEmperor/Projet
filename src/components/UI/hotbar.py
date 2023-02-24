import pygame

from src.services.visualization_service import VisualizationService
from src.config import Config
from src.global_state import GlobalState
from src.components.status import PlayerStatus

vec = pygame.math.Vector2

class Hotbar:
    def __init__(self):
        self.image = VisualizationService.get_hotbar_image()
        self.rect = self.image.get_rect()
        self.rect.center = vec(int(Config.WIDTH/2), Config.HEIGHT-50) # type: ignore        
        self.select_image = VisualizationService.get_select_hotbar_image()
        self.selected = None

    def draw(self, SCREEN, player):
        SCREEN.blit(self.image, self.rect)
        items = player.inventory.in_hotbar
        for i in range(len(items)):
            items[i].rect.topleft = vec(self.rect.topleft[0]+i*64,self.rect.topleft[1])
            SCREEN.blit(items[i].image, items[i].rect)
            if(items[i] == self.selected):
                SCREEN.blit(self.select_image, items[i].rect)
        
        size=100
        l=20
        pygame.draw.rect(SCREEN, (255,0,0), (int(Config.WIDTH/2-size/2),int(Config.HEIGHT-100-l), size, l)) # NEW
        pygame.draw.rect(SCREEN, (0,128,0), (int(Config.WIDTH/2-size/2), int(Config.HEIGHT-100-l), int(size*player.health/player.max_health), l)) # NEW
            

    def click_event(self, events, player, map):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for item in player.inventory.in_hotbar:
                    if(item.rect.collidepoint(pygame.mouse.get_pos())):
                        if(self.selected==item):
                            player.weapon = None
                            self.selected=None
                            map.attack_tiles=[]
                            GlobalState.PLAYER_STATE = PlayerStatus.MOVEMENT
                        else:
                            player.weapon = item
                            self.selected=item
                            map.attack_tiles=map.create_tile_list(item.range, player)
                            GlobalState.PLAYER_STATE = PlayerStatus.ATTACK