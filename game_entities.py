import pygame


class GameEntities:
    def __init__(self):
        self.all_entities = []
        self.ants = pygame.sprite.Group()
        self.spiders = pygame.sprite.Group()
        self.sugar = pygame.sprite.Group()

    def add_ant(self, ant):
        self.all_entities.append(ant)
        self.ants.add(ant)

    def add_spider(self, spider):
        self.all_entities.append(spider)
        self.spiders.add(spider)

    def add_sugar(self, sugar):
        self.all_entities.append(sugar)
        self.sugar.add(sugar)

    def clear(self):
        self.all_entities.clear()
        self.ants.empty()
        self.spiders.empty()
        self.sugar.empty()
