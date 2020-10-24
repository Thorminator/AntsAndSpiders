import pygame
import game_rules
from abc import abstractmethod
from vector import Vector


class Entity(pygame.sprite.Sprite):
    def __init__(self, size, start_pos, move_speed):
        super().__init__()
        surf = pygame.Surface(size)
        self.rect = surf.get_rect(center=start_pos)
        self.move_direction = Vector((0, 0))
        self.speed = move_speed

    def update(self, entities, score_counter, action=None):
        if not self.alive():
            return

        if action is not None:
            new_direction = self.__get_move_vector_from_action(action)
        else:
            new_direction = self.get_move_direction(entities)
        new_direction = new_direction.normalize().multiply(self.speed)
        if game_rules.USE_ACCELERATION:
            self.move_direction = self.move_direction.multiply(
                game_rules.ACCELERATION_DECAY).plus(new_direction)
        else:
            self.move_direction = new_direction
        self.rect.move_ip(self.move_direction.values)

    @staticmethod
    def __get_move_vector_from_action(action):
        return Vector((action[0], action[1]))

    @abstractmethod
    def get_move_direction(self, entities):
        pass

    def draw(self, surface):
        rotation = get_image_rotation_from_direction(self.move_direction)
        if self.get_image():
            image = pygame.transform.rotate(self.get_image(), rotation)
            surface.blit(image, self.rect)

    @abstractmethod
    def get_image(self):
        pass

    @property
    def x(self):
        return self.rect.centerx

    @x.setter
    def x(self, x):
        self.rect.centerx = x

    @property
    def y(self):
        return self.rect.centery

    @y.setter
    def y(self, y):
        self.rect.centery = y

    def get_state(self):
        state = {
            "position": (self.x, self.y),
            "move_direction": self.move_direction,
            "groups": self.groups()
        }
        return state

    def set_state(self, state):
        self.rect.center = state["position"]
        self.move_direction = state["move_direction"]
        self.kill()
        self.add(state["groups"])

    def get_observation(self):
        return self.x / game_rules.GAME_AREA_WIDTH, self.y / game_rules.GAME_AREA_HEIGHT, 1 if self.alive() else 0


DOWN_VECTOR = Vector((0, -1))


def get_image_rotation_from_direction(direction):
    rotation = DOWN_VECTOR.angle_to(direction)
    if direction.values[0] > 0:
        rotation = 360 - rotation
    return rotation


def load_scaled_image(image_path, scale):
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, scale)
