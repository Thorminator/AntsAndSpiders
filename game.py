import numpy as np
import pygame
import sys
import game_rules
from ant import Ant
from game_graphics import GameGraphics
from game_graphics import NoGraphics
from random_point_generator import RandomPointGenerator
from spider import Spider
from sugar import Sugar
from game_score import GameScore
from game_entities import GameEntities


class Game:
    def __init__(self, target_fps=60, simulate=False):
        self.target_fps = target_fps
        self.simulating = simulate
        self.entities = GameEntities()
        self.score_counter = GameScore()
        if not self.simulating:
            self.graphics = GameGraphics(self.entities, self.score_counter)
        else:
            self.graphics = NoGraphics()
        self.clock = pygame.time.Clock()
        self.paused = False
        self.game_over = False
        self.saved_state = None
        self.__setup_entities()
        self.__randomize_entity_positions()
        self.initial_state = self.get_state()

    def __setup_entities(self):
        self.__add_entities(Sugar, game_rules.SUGAR_COUNT, self.entities.add_sugar)
        self.__add_entities(Ant, game_rules.ANT_COUNT, self.entities.add_ant)
        self.__add_entities(Spider, game_rules.SPIDER_COUNT, self.entities.add_spider)

    def reset(self):
        self.set_state(self.initial_state)
        self.__randomize_entity_positions()

    def __randomize_entity_positions(self):
        point_generator = RandomPointGenerator(
            points_to_generate=game_rules.ANT_COUNT + game_rules.SPIDER_COUNT + game_rules.SUGAR_COUNT, min_distance=50)
        for entity in self.entities.all_entities:
            entity.x, entity.y = point_generator.get_next_point()

    @staticmethod
    def __add_entities(entity_class, entity_count, entity_adder, **kwargs):
        for i in range(entity_count):
            entity = entity_class(position=(0, 0), **kwargs)
            entity_adder(entity)

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                if event.key == pygame.K_r:
                    self.reset()
                if event.key == pygame.K_s:
                    self.saved_state = self.get_state()
                if event.key == pygame.K_d and self.saved_state:
                    self.set_state(self.saved_state)

    def __update_all(self, action=None):
        i = 0
        for entity in self.entities.all_entities:
            if isinstance(entity, Ant) and action is not None:
                entity.update(self.entities, self.score_counter, action[i:i+1][0])
                i += 1
            else:
                entity.update(self.entities, self.score_counter)
            self.score_counter.update()

    def __check_and_set_game_over(self):
        self.game_over = len(self.entities.ants) == 0 or len(self.entities.sugar) == 0
        if self.game_over:
            self.graphics.draw_game_over()

    def run_game(self):
        while not (self.game_over and self.simulating):
            self.clock.tick(self.target_fps)
            self.__handle_events()
            if not self.game_over:
                if not self.paused:
                    self.__update_all()
                self.graphics.draw_game(self.paused)
                self.__check_and_set_game_over()
        return self.score_counter.get_score()

    def get_state(self):
        state = {
            "entities_state": self.entities.get_state(),
            "score_counter_state": self.score_counter.get_state(),
            "paused": self.paused,
            "game_over": self.game_over
        }
        return state

    def set_state(self, state):
        self.entities.set_state(state["entities_state"])
        self.score_counter.set_state(state["score_counter_state"])
        self.paused = state["paused"]
        self.game_over = state["game_over"]

    def get_observation(self):
        return np.array([entity.get_observation() for entity in self.entities.all_entities], dtype=np.float32)

    def apply_action(self, action):
        if self.game_over:
            self.reset()
            return True
        self.__update_all(self.scale_action(action))
        self.graphics.draw_game()
        self.__check_and_set_game_over()
        return False

    @staticmethod
    def scale_action(action):
        return action * 2 - 1

    def get_score(self):
        return self.score_counter.get_score()

    def get_reward(self):
        return self.score_counter.get_reward()
