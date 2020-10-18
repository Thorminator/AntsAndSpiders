from game import game_rules
from vector.vector import Vector


def sum_vectors(vectors):
    """
    Calculates the sum of the given vectors.
    It is assumed that all vectors have the same dimensions
    :param vectors: The vectors to sum
    :return: Sum of the given vectors
    """
    if len(vectors) == 0:
        return Vector((0, 0))
    if len(vectors) == 1:
        return vectors[0]
    return Vector(tuple(sum(coordinate) for coordinate in zip(*(vector.values for vector in vectors))))


def vector_between_entities(entity1, entity2):
    """
    :return: A vector pointing from 'entity1' to 'entity2'.
    """
    return Vector((entity2.x - entity1.x, entity2.y - entity1.y))


def vector_between_points(p1, p2):
    """
    Get a vector pointing from p1 to p2.
    :param p1: The first point, as tuple of coordinates.
    :param p2: The second point, as a tuple of coordinates.
    :return: A new vector pointing from p2 to p1.
    """
    return Vector(tuple((x2 - x1 for x1, x2 in zip(p1, p2))))


def get_vectors_to_entities(entity, other_entities):
    """
    :param entity: The entity whose position is used to get vectors from
    :param other_entities: The entities to get vectors to. If 'entity' is in 'other_entities', it will be ignored.
    :return: A list with one vector for each entity in 'other_entities' pointing from the given 'entity' to that entity.
    """
    entities_except_self = [other_entity for other_entity in other_entities if other_entity != entity]
    return [vector_between_entities(entity, other_entity) for other_entity in entities_except_self]


def get_vectors_from_ant_to_walls(ant):
    """
    Get a list of vectors pointing to each wall in the game area.
    :param ant: The ant whose position is used to calculate wall vectors.
    :return: A list of vectors pointing from 'ant' to the walls of the game area.
    """
    return [Vector((-ant.x, 0)), Vector((game_rules.GAME_AREA_WIDTH - ant.x, 0)),
            Vector((0, -ant.y)), Vector((0, game_rules.GAME_AREA_HEIGHT - ant.y))]


def filter_entities_by_distance_to_entity(entities, target, max_distance, exclude=None):
    """
    Filter the list of 'entities', including only those that are at most 'max_distance' away from the 'target'.
    If exclude is set, that value will be filtered from the 'entities' list no matter what.
    :param entities: The list of entities to filter.
    :param target: The target to filter based on distance to.
    :param max_distance: The maximum distance that entities may have to the target.
    :param exclude: An entity to filter from the result list no matter what.
    :return: A list of entities, filtered such that only entities within max distance are included.
    """
    if exclude:
        entities = [entity for entity in entities if entity != exclude]
    entities_and_vectors = zip(entities, get_vectors_to_entities(target, entities))
    return [entity for entity, vector in entities_and_vectors if vector.length() <= max_distance]
