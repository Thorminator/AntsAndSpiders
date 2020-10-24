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

    def get_state(self):
        return [entity.get_state() for entity in self.all_entities]

    def set_state(self, state):
        for entity, entity_state in zip(self.all_entities, state):
            entity.set_state(entity_state)

    @staticmethod
    def __get_group_from_living_instance(entities, clazz):
        return next((group for group in
                     (entity.groups() for entity in entities if isinstance(entity, clazz) and entity.living)),
                    default=pygame.sprite.Group())
