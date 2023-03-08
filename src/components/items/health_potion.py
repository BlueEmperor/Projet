from src.services.visualization_service import VisualizationService

class HealthPotion:
    def __init__(self):
        self.image = VisualizationService.get_potion_image()
        self.rect = self.image.get_rect()
        self.usage = 1
        self.heal = 5
        self.type = 'potion'
    
    def use(self, entity):
        if(entity.health + self.heal>entity.max_health):
            entity.health = entity.max_health
            return
        entity.health += self.heal