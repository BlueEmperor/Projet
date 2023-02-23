import pygame

from path import ASSETS_DIR
from src.config import Config

pygame.font.init()

class VisualizationService:
    @staticmethod
    def get_player_image():
        return(pygame.image.load(ASSETS_DIR / "player.png").convert_alpha())

    @staticmethod
    def get_map_image():
        return(pygame.image.load(ASSETS_DIR / "map.png").convert_alpha())
    
    @staticmethod
    def get_squelette_image():
        return(pygame.image.load(ASSETS_DIR / "squelette.png").convert_alpha())

    @staticmethod
    def get_vampire_image():
        return(pygame.image.load(ASSETS_DIR / "vampire.png").convert_alpha())
    
    @staticmethod
    def get_red_select_image():
        return(pygame.image.load(ASSETS_DIR / "red_select.png").convert_alpha())
    
    @staticmethod
    def get_main_font():
        return(pygame.font.Font(None, 30))

    @staticmethod
    def load_main_game_displays():
        pygame.display.set_caption("Don't Touch My Presents")
        gift = VisualizationService.get_player_image()
        pygame.display.set_icon(gift)

    @staticmethod
    def draw_background_with_scroll(screen, scroll):
        background = VisualizationService.get_background_image()
        screen.blit(background, (0, scroll))

    @staticmethod
    def draw_author_credits(screen):
        credit_font = VisualizationService.get_credit_font_font()
        author_credits = credit_font.render("©GOODGIS 2022", True, (0, 0, 0))
        credits_rect = author_credits.get_rect(center=(Config.WIDTH // 2, 620))
        screen.blit(author_credits, credits_rect)

    @staticmethod
    def draw_best_score(screen, max_score):
        score_font = VisualizationService.get_score_font()
        best_score = score_font.render(f"Best: {max_score}", True, (0, 0, 0))
        best_score_rect = best_score.get_rect(center=(Config.WIDTH // 2, 220))
        screen.blit(best_score, best_score_rect)

    @staticmethod
    def draw_title(screen):
        y = sine(200.0, 1280, 10.0, 100)
        title = VisualizationService.get_title_image()
        screen.blit(title, (0, y))
        holding_gift = VisualizationService.get_holding_gift_image()
        screen.blit(holding_gift, (0, 320))

    @staticmethod
    def draw_press_key(screen, press_y):
        press_key = VisualizationService.get_press_key_image()
        screen.blit(press_key, (0, press_y))

    @staticmethod
    def draw_main_menu(screen, max_score, press_y):
        VisualizationService.draw_author_credits(screen)
        VisualizationService.draw_best_score(screen, max_score)
        VisualizationService.draw_title(screen)
        VisualizationService.draw_press_key(screen, press_y)
