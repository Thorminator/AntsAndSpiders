SCORE_UPDATE_AFTER = 500


class GameScore:
    def __init__(self):
        self.points = 0
        self.ticks = 0
        self.reward = 0

    def update(self):
        self.ticks += 1

    def add_points(self, points):
        self.points += points
        self.reward += points

    def get_score(self):
        return int(max(self.points - self.ticks / 20, 0))

    def get_reward(self):
        reward = self.reward
        self.reward = 0
        return reward + 1

    def reset(self):
        self.points = 0
        self.ticks = 0

    def get_state(self):
        return {
            "points": self.points,
            "ticks": self.ticks,
            "reward": self.reward,
        }

    def set_state(self, state):
        self.points = state["points"]
        self.ticks = state["ticks"]
        self.reward = state["reward"]
