import pygame
from entities import entity
from game import game_rules
from my_ant.my_ant import get_ant_direction


def collided_except_self(e1, e2):
    if e1 == e2:
        return False
    return pygame.sprite.collide_circle(e1, e2)


class Ant(entity.Entity):
    def __init__(self, position, entities):
        collision_size = (game_rules.ANT_COLLISION_DIAMETER, game_rules.ANT_COLLISION_DIAMETER)
        super().__init__(size=collision_size, start_pos=position, move_speed=game_rules.ANT_SPEED)
        image_size = (25, 25)
        self.image = self.load_scaled_image("./images/ant.png", image_size)
        self.dead_image = self.load_scaled_image("./images/dead_ant.png", image_size)
        self.entities = entities

    def update(self):
        super().update()

        if not self.alive():
            return

        self.gather_sugar()
        self.kill_if_outside_game_area()
        self.kill_if_colliding_with_other_entity()

    def gather_sugar(self):
        collided_sugar = pygame.sprite.spritecollide(self,
                                                     self.entities.sugar,
                                                     dokill=False,
                                                     collided=pygame.sprite.collide_circle)
        for sugar in collided_sugar:
            sugar.consume(game_rules.ANT_SUGAR_CONSUMPTION)

    def kill_if_outside_game_area(self):
        if not self.is_inside_game_area():
            self.kill()

    def is_colliding_with_ant(self):
        return pygame.sprite.spritecollideany(self, self.entities.ants, collided=collided_except_self)

    def is_inside_game_area(self):
        return 0 <= self.rect.left \
               and self.rect.right <= game_rules.GAME_AREA_WIDTH \
               and 0 <= self.rect.top \
               and self.rect.bottom <= game_rules.GAME_AREA_HEIGHT

    def kill_if_colliding_with_other_entity(self):
        if self.is_colliding_with_spider() or self.is_colliding_with_ant():
            self.kill()

    def is_colliding_with_spider(self):
        return pygame.sprite.spritecollideany(self, self.entities.spiders,
                                              collided=pygame.sprite.collide_circle)

    def get_move_direction(self):
        return get_ant_direction(self, self.entities)

    def get_image(self):
        if self.alive():
            return self.image
        else:
            return self.dead_image
