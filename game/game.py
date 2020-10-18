import pygame
import sys
from game import game_rules
from entities.ant import Ant
from game.game_graphics import GameGraphics
from game.game_graphics import NoGraphics
from game.random_point_generator import RandomPointGenerator
from entities.spider import Spider
from entities.sugar import Sugar
from game.game_score import GameScore
from game.game_entities import GameEntities


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

    def reset(self):
        self.entities.clear()
        self.score_counter.reset()
        self.paused = False
        self.game_over = False
        self.__setup()

    def __setup(self):
        point_generator = RandomPointGenerator(
            points_to_generate=game_rules.ANT_COUNT + game_rules.SPIDER_COUNT + game_rules.SUGAR_COUNT, min_distance=50)
        self.__add_entities(Sugar, game_rules.SUGAR_COUNT, self.entities.add_sugar, point_generator,
                            score_counter=self.score_counter)
        self.__add_entities(Ant, game_rules.ANT_COUNT, self.entities.add_ant, point_generator, entities=self.entities)
        self.__add_entities(Spider, game_rules.SPIDER_COUNT, self.entities.add_spider, point_generator,
                            entities=self.entities)

    @staticmethod
    def __add_entities(entity_class, entity_count, entity_adder, point_generator, **kwargs):
        for i in range(entity_count):
            entity = entity_class(position=point_generator.get_next_point(), **kwargs)
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

    def __update_all(self):
        for entity in self.entities.all_entities:
            entity.update()
            self.score_counter.update(self.clock.get_time())

    def __check_and_set_game_over(self):
        self.game_over = len(self.entities.ants) == 0 or len(self.entities.sugar) == 0
        if self.game_over:
            self.graphics.draw_game_over()

    def run_game(self):
        self.reset()
        while not (self.game_over and self.simulating):
            self.clock.tick(self.target_fps)
            self.__handle_events()
            if not self.game_over:
                if not self.paused:
                    self.__update_all()
                self.graphics.draw_game(self.paused)
                self.__check_and_set_game_over()
        return self.score_counter.get_updated_score()
