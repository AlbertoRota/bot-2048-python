import unittest
import numpy as np
from bot.game.game import Game


class TestGameMethods(unittest.TestCase):
    def test_swipe_row_left(self):
        np.testing.assert_array_equal(Game.__swipe_row_left___([2, 2, 0, 0]), [4, 0, 0, 0])
        np.testing.assert_array_equal(Game.__swipe_row_left___([0, 0, 0, 0]), [0, 0, 0, 0])
        np.testing.assert_array_equal(Game.__swipe_row_left___([2, 4, 0, 0]), [2, 4, 0, 0])
        np.testing.assert_array_equal(Game.__swipe_row_left___([8, 0, 0, 8]), [16, 0, 0, 0])
        np.testing.assert_array_equal(Game.__swipe_row_left___([2, 2, 4, 8]), [4, 4, 8, 0])

    def test_swipe_grid(self):
        grid = [[2, 2, 0, 0], [0, 0, 0, 0], [2, 4, 0, 0], [2, 2, 4, 8]]
        grid_left = [[4, 0, 0, 0], [0, 0, 0, 0], [2, 4, 0, 0], [4, 4, 8, 0]]
        grid_down = [[0, 0, 0, 0], [0, 2, 0, 0], [2, 4, 0, 0], [4, 2, 4, 8]]
        grid_right = [[0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 2, 4], [0, 4, 4, 8]]
        grid_up = [[4, 2, 4, 8], [2, 4, 0, 0], [0, 2, 0, 0], [0, 0, 0, 0]]

        np.testing.assert_array_equal(Game.swipe_grid(grid, "LEFT"), grid_left)
        np.testing.assert_array_equal(Game.swipe_grid(grid, "DOWN"), grid_down)
        np.testing.assert_array_equal(Game.swipe_grid(grid, "RIGHT"), grid_right)
        np.testing.assert_array_equal(Game.swipe_grid(grid, "UP"), grid_up)

    def test_is_valid_move(self):
        grid = [[2, 2, 0, 4], [4, 8, 0, 2], [2, 4, 0, 4], [4, 8, 0, 8]]

        self.assertTrue(Game.is_valid_move(grid, "LEFT"))
        self.assertFalse(Game.is_valid_move(grid, "DOWN"))
        self.assertTrue(Game.is_valid_move(grid, "RIGHT"))
        self.assertFalse(Game.is_valid_move(grid, "UP"))

    def test_is_game_over(self):
        grid_ok = [[2, 2, 0, 4], [4, 8, 0, 2], [2, 4, 0, 4], [4, 8, 0, 8]]
        grid_ko = [[2, 4, 2, 4], [4, 8, 4, 2], [2, 4, 8, 4], [4, 8, 2, 8]]

        self.assertFalse(Game.is_game_over(grid_ok))
        self.assertTrue(Game.is_game_over(grid_ko))
