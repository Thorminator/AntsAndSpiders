import sys
import re
from web import online_score
import os
from game.game import Game
import multiprocessing as mp

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
USERNAME_PATTERN = re.compile(r"-username=(\w+)$")


def run_simulation(_):
    return Game(target_fps=0, simulate=True).run_game()


def get_username():
    names = [arg for arg in sys.argv if USERNAME_PATTERN.match(arg)]
    if len(names) == 1:
        return USERNAME_PATTERN.match(names[0]).group(1)
    else:
        return None


def benchmark():
    pool = mp.Pool(mp.cpu_count())
    scores = pool.map(run_simulation, [i for i in range(200)])
    pool.close()
    benchmark_score = int(sum(scores) / len(scores))
    print(f"Your benchmark score is: {benchmark_score} points.")
    username = get_username()
    if username:
        online_score.save_score(username, benchmark_score)


def run_game():
    Game(target_fps=60, simulate=False).run_game()


if __name__ == "__main__":
    if any(arg == "-benchmark" for arg in sys.argv):
        benchmark()
    else:
        run_game()
