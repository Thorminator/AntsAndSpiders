import entity
from entity import load_scaled_image
import game_rules
from vector import Vector


class Sugar(entity.Entity):
    size = (50, 50)
    images = [load_scaled_image("./images/sugar_3.png", size),
              load_scaled_image("./images/sugar_2.png", size),
              load_scaled_image("./images/sugar_1.png", size)]

    def __init__(self, position):
        super().__init__((50, 50), position, 0)
        self.initial_amount = self.amount = game_rules.INIT_SUGAR_AMOUNT

    def get_move_direction(self, entities):
        return Vector((0, 0))

    def get_image(self):
        if not self.alive():
            return None

        image_count = len(Sugar.images)
        index = min(int(self.amount / self.initial_amount * image_count), image_count - 1)
        return Sugar.images[index]

    def consume(self, score_counter, amount):
        amount_consumed = min(self.amount, amount)
        self.amount -= amount_consumed
        score_counter.add_points(amount_consumed)
        if self.amount <= 0:
            self.kill()

    def get_state(self):
        state = super().get_state()
        state["sugar_amount"] = self.amount
        return state

    def set_state(self, state):
        super().set_state(state)
        self.amount = state["sugar_amount"]

    def get_observation(self):
        return self.x / game_rules.GAME_AREA_WIDTH, self.y / game_rules.GAME_AREA_HEIGHT, self.amount / self.initial_amount
