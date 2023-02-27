import pygame
from time import sleep

from src.components.entities.entity import Entity
from src.config import Config
from src.components.map import Map
from src.services.visualization_service import VisualizationService
from src.components.UI.inventory import Inventory
from src.global_state import GlobalState
from src.components.status import GameStatus

vec = pygame.math.Vector2

class Player(Entity):
    def __init__(self, map_pos = vec(8,2),pv=20):
        super().__init__()
        self.image = VisualizationService.get_player_image()
        self.rect = self.image.get_rect()
        self.pos = vec(int(Config.WIDTH/2),int(Config.HEIGHT/2))
        self.rect.center = self.pos # type: ignore
        self.map_pos = map_pos
        self.max_health = pv
        self.health = pv
        self.inventory = Inventory()
        self.weapon = self.inventory.in_hotbar[0]
        self.gold = 0

    def lost_game(self):
        if(self.health <= 0):
            GlobalState.GAME_STATE = GameStatus.GAME_END

    def move_input(self, map, entities_objects, damage_list):
        keys=pygame.key.get_pressed()
        for key in Map.dir.keys():
            if(keys[key] and not(self.is_moving) and map.is_empty(Map.dir[key]+self.map_pos) and Entity.check_if_moving(entities_objects)):
                sleep(0.04)
                self.move(map,Map.dir[key]+self.map_pos,Map.dir[key],  False)
                for i in range(len(entities_objects)):
                    entities_objects[i].move_tick=(i+1)*15
                Entity.play(map, entities_objects, self, damage_list)