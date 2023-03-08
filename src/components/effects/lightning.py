from src.services.visualization_service import VisualizationService

class Lightning:
    def __init__(self, pos):
        self.image_list = VisualizationService.get_lightning_image_list()
        self.image = self.image_list[0][0]
        self.animation_tick = self.image_list[0][1]
        self.animation_frame = 0
        self.pos = pos