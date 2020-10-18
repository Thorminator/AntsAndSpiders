import entity
import game_rules
import game_score
from vector import Vector


class Sugar(entity.Entity):
    def __init__(self, position, score_counter):
        size = (50, 50)
        super().__init__(size, position, 0)
        self.initial_amount = self.amount = game_rules.INIT_SUGAR_AMOUNT
        self.images = [self.load_scaled_image("./images/sugar_3.png", size),
                       self.load_scaled_image("./images/sugar_2.png", size),
                       self.load_scaled_image("./images/sugar_1.png", size)]
        self.score_counter = score_counter

    def get_move_direction(self):
        return Vector((0, 0))

    def get_image(self):
        if not self.alive():
            return None

        index = min(int(self.amount / self.initial_amount * len(self.images)), len(self.images) - 1)
        return self.images[index]

    def consume(self, amount):
        amount_consumed = min(self.amount, amount)
        self.amount -= amount_consumed
        self.score_counter.sugar_collected += amount_consumed
        if self.amount <= 0:
            self.kill()
