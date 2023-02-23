from src.global_state import GlobalState

def draw_sprites(sprites):
    for sprite in sprites:
        sprite.draw(GlobalState.SCREEN)
