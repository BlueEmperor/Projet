import pygame
from time import sleep

from src.components.entities.entity import Entity
from src.config import Config
from src.components.map import Map
from src.services.visualization_service import VisualizationService
from src.global_state import GlobalState
from src.components.node import Node

vec = pygame.math.Vector2

class Player(Entity):
    def __init__(self, map_pos = vec(1,1),pv=20):
        self.is_moving = False
        self.image = VisualizationService.get_player_image()
        self.rect = self.image.get_rect()
        self.pos = vec(int(Config.WIDTH/2),int(Config.HEIGHT/2))
        self.rect.center = self.pos # type: ignore
        self.map_pos = map_pos
        self.max_health = pv
        self.health = pv

    
    def update(self, map, entities_objects):
        self.move_animation(map, self, entities_objects)

        keys=pygame.key.get_pressed()
        for key in Map.dir.keys():
            if(keys[key] and not(self.is_moving) and map.is_empty(Map.dir[key]+self.map_pos) and Entity.check_if_moving(entities_objects)):
                self.move(map,Map.dir[key]+self.map_pos,Map.dir[key],  False)
                for i in range(len(entities_objects)):
                    entities_objects[i].move_tick=(i+1)*6
                Entity.play(map, entities_objects, self)