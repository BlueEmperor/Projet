import pygame

from src.components.entities.entity import Entity
from src.services.visualization_service import VisualizationService
from src.config import Config
from src.components.map import Map
from src.global_state import GlobalState

vec = pygame.math.Vector2

class Vampire(Entity):
    def __init__(self, player_pos, map_pos, map, pv=14, damage=2):
        super().__init__()
        self.image = VisualizationService.get_vampire_image()
        self.rect = self.image.get_rect()
        self.pos = vec(int(Config.WIDTH/2),int(Config.HEIGHT/2))-(player_pos-map_pos)*48
        self.rect.center = self.pos
        self.map_pos = map_pos
        self.max_health = pv
        self.health = pv
        self.damage = damage
        map.put(self.map_pos)
        