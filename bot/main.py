import numpy as np
from bot.game.game import Game
from bot.ai.random_ai import RandomAi
from bot.ai.ordered_ai import OrderedAi


def main():
    rnd_initial_grid = Game.spawn_tile(Game.spawn_tile(
        np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    ))

    game = Game(rnd_initial_grid)
    num_of_movements = 0
    while not game.is_game_over:
        direction = OrderedAi.get_next_move(game)
        print("Grid: ")
        print(game.grid)
        print("Direction: " + direction)
        print()
        game = Game(Game.spawn_tile(game.swipe_grid(direction)))
        num_of_movements += 1

    print("Total movements = " + str(num_of_movements))
    print("Final grid = ")
    print(game.grid)


if __name__ == '__main__':
    main()
