import entity
from entity import load_scaled_image
import game_rules
import util
from vector import Vector


class Spider(entity.Entity):
    image = load_scaled_image("./images/spider.png", (50, 50))

    def __init__(self, position):
        size = (game_rules.SPIDER_COLLISION_DIAMETER, game_rules.SPIDER_COLLISION_DIAMETER)
        super().__init__(size=size, start_pos=position, move_speed=game_rules.SPIDER_SPEED)

    def get_move_direction(self, entities):
        vectors_to_ants = util.get_vectors_to_entities(self, entities.ants)
        vectors_to_ants = sorted(vectors_to_ants, key=lambda v: v.length())
        if len(vectors_to_ants) == 0:
            return Vector((0, 0))
        return vectors_to_ants[0]

    def get_image(self):
        return Spider.image
