import game_rules
import random
import math


class PointGenerator:
    def __init__(self, points_to_generate, min_distance):
        self.points_to_generate = points_to_generate
        self.min_distance = min_distance
        self.points = self.__generate_points()

    def __generate_points(self):
        generated_points = []
        for _ in range(self.points_to_generate):
            generated_points.append(self.__generate_point(generated_points))
        return generated_points

    def __generate_point(self, existing_points):
        x = random.randint(self.min_distance, game_rules.GAME_AREA_WIDTH - self.min_distance)
        y = random.randint(self.min_distance, game_rules.GAME_AREA_HEIGHT - self.min_distance)
        point = (x, y)
        if self.__is_valid_point(point, existing_points):
            return point
        else:
            return self.__generate_point(existing_points)

    def __is_valid_point(self, point, existing_points):
        distances = tuple(math.sqrt((point[0] - x) ** 2 + (point[1] - y) ** 2) for (x, y) in existing_points)
        return all(dist > self.min_distance for dist in distances)

    def get_point(self):
        if len(self.points) > 0:
            choice = random.choice(self.points)
            self.points.remove(choice)
            return choice
        else:
            raise ValueError("No more points in generator")
