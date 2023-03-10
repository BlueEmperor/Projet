import pygame

from src.services.visualization_service import VisualizationService

class BasicSword:
    def __init__(self):
        self.image = VisualizationService.get_sword_icon_image()
        self.rect = self.image.get_rect()
        self.range = (1,1)
        self.range_type = "around"
        self.damage = 2
        self.type = "sword"