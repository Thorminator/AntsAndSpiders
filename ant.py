import pygame
import entity
from entity import load_scaled_image
import game_rules
from my_ant import get_ant_direction


def collided_except_self(e1, e2):
    if e1 == e2:
        return False
    return pygame.sprite.collide_circle(e1, e2)


class Ant(entity.Entity):
    image_size = (25, 25)
    image = load_scaled_image("./images/ant.png", image_size)
    dead_image = load_scaled_image("./images/dead_ant.png", image_size)

    def __init__(self, position):
        collision_size = (game_rules.ANT_COLLISION_DIAMETER, game_rules.ANT_COLLISION_DIAMETER)
        super().__init__(size=collision_size, start_pos=position, move_speed=game_rules.ANT_SPEED)

    def update(self, entities, score_counter, action=None):
        super().update(entities, score_counter, action)

        if not self.alive():
            return

        self.gather_sugar(entities, score_counter)
        self.kill_if_outside_game_area()
        self.kill_if_colliding_with_other_entity(entities)

    def gather_sugar(self, entities, score_counter):
        collided_sugar = pygame.sprite.spritecollide(self,
                                                     entities.sugar,
                                                     dokill=False,
                                                     collided=pygame.sprite.collide_circle)
        for sugar in collided_sugar:
            sugar.consume(score_counter, game_rules.ANT_SUGAR_CONSUMPTION)

    def kill_if_outside_game_area(self):
        if not self.is_inside_game_area():
            self.kill()

    def is_colliding_with_ant(self, entities):
        return pygame.sprite.spritecollideany(self, entities.ants, collided=collided_except_self)

    def is_inside_game_area(self):
        return 0 <= self.rect.left \
               and self.rect.right <= game_rules.GAME_AREA_WIDTH \
               and 0 <= self.rect.top \
               and self.rect.bottom <= game_rules.GAME_AREA_HEIGHT

    def kill_if_colliding_with_other_entity(self, entities):
        if self.is_colliding_with_spider(entities) or self.is_colliding_with_ant(entities):
            self.kill()

    def is_colliding_with_spider(self, entities):
        return pygame.sprite.spritecollideany(self, entities.spiders,
                                              collided=pygame.sprite.collide_circle)

    def get_move_direction(self, entities):
        return get_ant_direction(self, entities)

    def get_image(self):
        if self.alive():
            return Ant.image
        else:
            return Ant.dead_image
