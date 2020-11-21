from game import game_rules
from game.game_rules import ANT_SPEED
from vector import util
from vector.vector import Vector

distraction_ants = []

avoid_ant_factor = 8
avoid_distraction_ant_factor = 2
avoid_spider_factor = 5
avoid_wall_factor = 10

ant_near_sugar_score = 100
ant_sugar_filter_dist = 100
spider_sugar_filter_dist = 200
spider_near_sugar_score = 300

distraction_ants_factor = 0.2
distraction_ant_spider_factor = 3
distraction_max_spider_dist = 75


def get_avoid_ants_vectors(ant, entities, distraction_ant=False):
    vectors = get_vectors_avoiding_entities(ant, entities.ants)
    actual_factor = avoid_distraction_ant_factor if distraction_ant else avoid_ant_factor
    return [v.normalize().multiply(actual_factor / v.length()) for v in vectors
            if v.length() < (ANT_SPEED*4 + game_rules.ANT_COLLISION_DIAMETER)]


def get_avoid_spiders_vectors(ant, entities):
    vectors = get_vectors_avoiding_entities(ant, entities.spiders)
    return [v.normalize().multiply(avoid_spider_factor / v.length()) for v in vectors if
            v.length() < (20 + game_rules.SPIDER_COLLISION_DIAMETER)]


def get_vectors_avoiding_entities(ant, entities):
    vectors_to_entities = util.get_vectors_to_entities(ant, entities)
    return [v.invert() for v in vectors_to_entities]


def get_avoid_walls_vectors(ant):
    vectors_to_walls = [v for v in util.get_vectors_from_ant_to_walls(ant)]
    return [v.invert().normalize().multiply(avoid_wall_factor / (v.length()**2)) for v in vectors_to_walls]


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


def get_stay_close_to_spider_vector(ant, entities):
    spider = entities.spiders.sprites()[0]
    ant_to_spider_vector = util.vector_between_entities(ant, spider)
    if ant_to_spider_vector.length() > distraction_max_spider_dist:
        return [ant_to_spider_vector.normalize().multiply(distraction_ant_spider_factor)]
    else:
        return get_avoid_spiders_vectors(ant, entities)


def get_distraction_vector(ant, entities):
    avoid_ants_vectors = get_avoid_ants_vectors(ant, entities, ant in distraction_ants)
    avoid_wall_vectors = get_avoid_walls_vectors(ant)
    stay_close_to_spider_vector = get_stay_close_to_spider_vector(ant, entities)
    return util.sum_vectors(avoid_ants_vectors + avoid_wall_vectors + stay_close_to_spider_vector)


def get_gatherer_vector(ant, entities):
    avoid_ants_vectors = get_avoid_ants_vectors(ant, entities)
    avoid_wall_vectors = get_avoid_walls_vectors(ant)
    avoid_spiders_vectors = get_avoid_spiders_vectors(ant, entities)
    gather_sugar_vector = get_sugar_vector(ant, entities)
    return util.sum_vectors(avoid_ants_vectors + avoid_wall_vectors + avoid_spiders_vectors + [gather_sugar_vector])


def get_ant_direction(ant, entities):
    for distract_ant in distraction_ants:
        if not distract_ant.alive():
            distraction_ants.remove(distract_ant)
    num_distraction_ants = int(distraction_ants_factor * len(entities.ants))

    if len(distraction_ants) < num_distraction_ants:
        distraction_ants.append(ant)

    if ant in distraction_ants:
        return get_distraction_vector(ant, entities)
    else:
        return get_gatherer_vector(ant, entities)