import pygame

from src.services.visualization_service import VisualizationService

cursor = VisualizationService.get_cursor_image()
cursor_rect = cursor.get_rect()

def DrawCursor(SCREEN):
    cursor_rect.center = pygame.mouse.get_pos()  # update position 
    SCREEN.blit(cursor, cursor_rect)