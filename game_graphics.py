from abc import abstractmethod

import pygame
import game_rules
import online_score

GAME_AREA_CENTER_X = game_rules.GAME_AREA_WIDTH / 2
GAME_AREA_CENTER_Y = game_rules.GAME_AREA_HEIGHT / 2
GAME_AREA_CENTER = (GAME_AREA_CENTER_X, GAME_AREA_CENTER_Y)

pygame.init()

SCREEN_SIZE = (game_rules.GAME_AREA_WIDTH, game_rules.GAME_AREA_HEIGHT)
WHITE = (255, 255, 255)
SCORE_FONT = pygame.font.SysFont("Verdana", 25)
SPLASH_FONT = pygame.font.SysFont("Verdana", 50)


class AbstractGraphics:
    @abstractmethod
    def draw_game(self, paused):
        pass

    @abstractmethod
    def draw_game_over(self):
        pass


class GameGraphics(AbstractGraphics):
    def __init__(self, entities, score_counter):
        self.entities = entities
        self.score_counter = score_counter
        self.screen = pygame.display.set_mode(SCREEN_SIZE)

    def draw_game(self, paused):
        self.screen.fill(WHITE)
        self.__draw_entities()
        self.__draw_score()
        if paused:
            self.__draw_text(SPLASH_FONT, "Paused", GAME_AREA_CENTER)
        pygame.display.update()

    def __draw_entities(self):
        for entity in self.entities.all_entities:
            entity.draw(self.screen)

    def __draw_score(self):
        text_surface = SCORE_FONT.render(f"Score: {str(self.score_counter.get_score())}", False, (0, 0, 0))
        self.screen.blit(text_surface, (0, 0))

    def __draw_text(self, font, text, position_center):
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=position_center)
        self.screen.blit(text_surface, text_rect)

    def draw_game_over(self):
        self.screen.fill(WHITE)
        self.__draw_entities()
        self.__draw_text(SPLASH_FONT, f"Your score: {self.score_counter.get_updated_score()}",
                         (GAME_AREA_CENTER_X, 100))
        scores = online_score.get_scores()
        if scores:
            self.__draw_text(SCORE_FONT, "Benchmark high scores:", (GAME_AREA_CENTER_X, 200))
            self.__draw_score_list(scores)
        pygame.display.update()

    def __draw_score_list(self, scores):
        sorted_users_and_scores = sorted([(entry["username"], entry["score"]) for entry in scores],
                                         key=lambda t: t[1], reverse=True)
        top_ten_users_and_scores = sorted_users_and_scores[0:10]
        for index, (username, score) in enumerate(top_ten_users_and_scores):
            self.__draw_text(SCORE_FONT, f"{index + 1}. {username}: {score}", (GAME_AREA_CENTER_X, 250 + 50 * index))


class NoGraphics(AbstractGraphics):
    def draw_game(self, paused):
        pass

    def draw_game_over(self):
        pass
