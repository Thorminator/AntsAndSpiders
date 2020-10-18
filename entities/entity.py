import pygame
from game import game_rules
from abc import abstractmethod
from vector.vector import Vector


class Entity(pygame.sprite.Sprite):
    def __init__(self, size, start_pos, move_speed):
        super().__init__()
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(center=start_pos)
        self.move_direction = Vector((0, 0))
        self.speed = move_speed

    def update(self):
        if not self.alive():
            return

        new_direction = self.get_move_direction().normalize().multiply(self.speed)
        if game_rules.USE_ACCELERATION:
            self.move_direction = self.move_direction.multiply(
                game_rules.ACCELERATION_DECAY).plus(new_direction)
        else:
            self.move_direction = new_direction
        self.rect.move_ip(self.move_direction.values)

    @abstractmethod
    def get_move_direction(self):
        pass

    def draw(self, surface):
        rotation = get_image_rotation_from_direction(self.move_direction)
        if self.get_image():
            image = pygame.transform.rotate(self.get_image(), rotation)
            surface.blit(image, self.rect)

    @abstractmethod
    def get_image(self):
        pass

    @staticmethod
    def load_scaled_image(image_path, scale):
        image = pygame.image.load(image_path)
        return pygame.transform.scale(image, scale)

    @property
    def x(self):
        return self.rect.centerx

    @property
    def y(self):
        return self.rect.centery

    def get_size(self):
        return self.rect.size


DOWN_VECTOR = Vector((0, -1))


def get_image_rotation_from_direction(direction):
    rotation = DOWN_VECTOR.angle_to(direction)
    if direction.values[0] > 0:
        rotation = 360 - rotation
    return rotation
