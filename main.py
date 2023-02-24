import pygame
from sys import exit

from src.config import Config
from src.global_state import GlobalState
from src.components.status import GameStatus
from src.game_phases import main_menu_phase, gameplay_phase, end_menu_phase

pygame.init()

FramePerSec = pygame.time.Clock()

def update_game_display():
    pygame.display.update()
    FramePerSec.tick(Config.FPS)


def main():
    while True:
        events = pygame.event.get()
        if GlobalState.GAME_STATE == GameStatus.MAIN_MENU:
            main_menu_phase(events)
        elif GlobalState.GAME_STATE == GameStatus.GAMEPLAY:
            gameplay_phase(events)
        elif GlobalState.GAME_STATE == GameStatus.GAME_END:
            end_menu_phase(events)

        #MusicService.start_background_music()
        for event in events:
            if(event.type == pygame.QUIT):
                pygame.quit()
                exit()
        
        update_game_display()


if __name__ == "__main__":
    main()
