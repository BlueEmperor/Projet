import pygame

from src.services.visualization_service import VisualizationService

class BasicBow:
    def __init__(self):
        self.image = VisualizationService.get_bow_icon_image()
        self.rect = self.image.get_rect()
        self.range = (3,7)
        self.range_type = "around"
        self.damage = 3
