import pygame

from src.components.entities.entity import Entity
from src.components.items.boule_de_feu_staff import BdfStaff
from src.services.visualization_service import VisualizationService
from src.config import Config

vec = pygame.math.Vector2

class Squelette(Entity):
    def __init__(self, player_pos, map_pos, map, pv=10, damage=2):
        super().__init__()
        self.image = VisualizationService.get_squelette_image()
        self.rect = self.image.get_rect()
        self.pos = vec(int(Config.WIDTH/2),int(Config.HEIGHT/2))-(player_pos-map_pos)*48
        self.rect.center = self.pos
        self.map_pos = map_pos
        self.max_health = pv
        self.health = pv
        self.damage = damage
        self.weapon = BdfStaff()
        map.put(self.map_pos)
        