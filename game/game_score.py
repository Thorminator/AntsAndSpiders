SCORE_UPDATE_AFTER = 500


class GameScore:
    def __init__(self):
        self.sugar_collected = 0
        self.score_to_return = 0
        self.time_to_next_update = SCORE_UPDATE_AFTER
        self.ticks = 0

    def update(self, delta_time):
        self.ticks += 1
        self.time_to_next_update -= delta_time
        if self.time_to_next_update <= 0:
            self.__update_score_to_return()

    def __update_score_to_return(self):
        self.score_to_return = int(self.sugar_collected - min(1000, int(self.ticks / 200)))
        self.time_to_next_update = SCORE_UPDATE_AFTER

    def get_score(self):
        return self.score_to_return

    def get_updated_score(self):
        self.__update_score_to_return()
        return self.score_to_return

    def reset(self):
        self.sugar_collected = 0
        self.ticks = 0
