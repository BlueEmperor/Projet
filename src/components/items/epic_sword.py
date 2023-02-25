import pygame

from src.services.visualization_service import VisualizationService

class EpicSword:
    def __init__(self):
        self.image = VisualizationService.get_sword_icon_image()
        self.rect = self.image.get_rect()
        self.range = (1,2)
        self.damage = 7