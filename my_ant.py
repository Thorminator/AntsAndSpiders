import game_rules
import util
from vector import Vector


avoid_ant_factor = 8
avoid_spider_factor = 5
avoid_wall_factor = 7
ant_near_sugar_score = 100
ant_sugar_filter_dist = 100
spider_sugar_filter_dist = 200
spider_near_sugar_score = 300


def get_avoid_ants_vectors(ant, entities):
    vectors = get_vectors_avoiding_entities(ant, entities.ants)
    return [v.normalize().multiply(avoid_ant_factor / v.length()) for v in vectors if
            v.length() < (15 + game_rules.ANT_COLLISION_DIAMETER)]


def get_avoid_spiders_vectors(ant, entities):
    vectors = get_vectors_avoiding_entities(ant, entities.spiders)
    return [v.normalize().multiply(avoid_spider_factor / v.length()) for v in vectors if
            v.length() < (20 + game_rules.SPIDER_COLLISION_DIAMETER)]


def get_vectors_avoiding_entities(ant, entities):
    vectors_to_entities = util.get_vectors_to_entities(ant, entities)
    return [v.invert() for v in vectors_to_entities]


def get_avoid_walls_vectors(ant):
    vectors_to_walls = [v for v in util.get_vectors_from_ant_to_walls(ant) if
                        v.length() < (10 + game_rules.ANT_COLLISION_DIAMETER)]
    return [v.invert().normalize().multiply(1 / v.length()) for v in vectors_to_walls]


def get_sugar_score(ant, sugar, sugar_vector, entities):
    close_ant_count = len(
        util.filter_entities_by_distance_to_entity(entities.ants, sugar, ant_sugar_filter_dist, ant))
    close_spiders = len(
        util.filter_entities_by_distance_to_entity(entities.spiders, sugar, spider_sugar_filter_dist))
    return sugar_vector.length() + close_ant_count * ant_near_sugar_score + close_spiders * spider_near_sugar_score


def get_sugar_vector(ant, entities):
    sugar_and_vectors = [(sugar, (util.vector_between_entities(ant, sugar))) for sugar in entities.sugar]

    sorted_sugar_vectors = [vector for sugar, vector in
                            sorted(sugar_and_vectors,
                                   key=lambda sugar_and_vector:
                                   get_sugar_score(ant, sugar_and_vector[0], sugar_and_vector[1], entities))]
    if not sorted_sugar_vectors:
        return Vector((0, 0))
    return sorted_sugar_vectors[0].normalize().multiply(1 / 50)


def get_ant_direction(ant, entities):
    avoid_ants_vectors = get_avoid_ants_vectors(ant, entities)
    avoid_wall_vectors = get_avoid_walls_vectors(ant)
    avoid_spiders_vectors = get_avoid_spiders_vectors(ant, entities)
    gather_sugar_vector = get_sugar_vector(ant, entities)
    return util.sum_vectors(avoid_ants_vectors + avoid_wall_vectors + avoid_spiders_vectors + [gather_sugar_vector])
