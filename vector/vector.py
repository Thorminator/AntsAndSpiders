import math


class Vector:
    def __init__(self, coordinates):
        self.values = coordinates

    def length(self):
        """
        :return: The length of this vector.
        """
        return math.sqrt(sum([v ** 2 for v in self.values]))

    def invert(self):
        """
        :return: This vector inverted, such that it points in the opposite direction.
        """
        return Vector(tuple(-v for v in self.values))

    def add(self, n):
        """
        Create a new vector that is equal to this vector with a value added to all coordinates.
        :param n: The value to add.
        :return: A new vector, with 'n' added to each coordinate.
        """
        return Vector(tuple(v + n for v in self.values))

    def multiply(self, n):
        """
        Creates a new vector that is equal to this vector with all coordinates multiplied by a value.
        :param n: The value to multiply each coordinate by.
        :return: A new vector, with each coordinate multiplied by 'n'.
        """
        return Vector(tuple(v * n for v in self.values))

    def normalize(self):
        """
        :return: A vector that points in the same direction as this vector, but with a length of 1.
        """
        length = self.length()
        if length == 0:
            return Vector((0, 0))
        return self.multiply(1 / length)

    def dot_product(self, other):
        """
        :return: The dot product of this vector and 'other'.
        """
        return sum([v1 * v2 for (v1, v2) in zip(self.values, other.values)])

    def angle_to(self, other):
        """
        :return: The angle from this vector to 'other' in degrees.
        """
        product_of_lengths = self.length() * other.length()
        if product_of_lengths == 0:
            return 0
        dot_product = self.dot_product(other)
        return math.degrees(math.acos(clamp(-1, dot_product / product_of_lengths, 1)))

    def plus(self, other):
        """
        Add this vector to 'other' and return the result.
        :param other: The vector to add to this vector.
        :return: The result of adding this vector to 'other'.
        """
        if len(self.values) != len(other.values):
            raise ValueError(f"Cannot add vectors of different lengths")

        return Vector(tuple(a + b for a, b in zip(self.values, other.values)))


def clamp(minimum, x, maximum):
    """
    :return: The value 'x' clamped between 'minimum' and 'maximum'.
    """
    return max(minimum, min(x, maximum))