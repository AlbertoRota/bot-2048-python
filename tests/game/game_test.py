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
        grid = Game(np.array([[2, 2, 0, 0], [0, 0, 0, 0], [2, 4, 0, 0], [2, 2, 4, 8]]))
        grid_left = [[4, 0, 0, 0], [0, 0, 0, 0], [2, 4, 0, 0], [4, 4, 8, 0]]
        grid_down = [[0, 0, 0, 0], [0, 2, 0, 0], [2, 4, 0, 0], [4, 2, 4, 8]]
        grid_right = [[0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 2, 4], [0, 4, 4, 8]]
        grid_up = [[4, 2, 4, 8], [2, 4, 0, 0], [0, 2, 0, 0], [0, 0, 0, 0]]

        np.testing.assert_array_equal(grid.swipe_grid("LEFT"), grid_left)
        np.testing.assert_array_equal(grid.swipe_grid("DOWN"), grid_down)
        np.testing.assert_array_equal(grid.swipe_grid("RIGHT"), grid_right)
        np.testing.assert_array_equal(grid.swipe_grid("UP"), grid_up)

    def test_is_valid_move(self):
        grid = Game(np.array([[2, 2, 0, 4], [4, 8, 0, 2], [2, 4, 0, 4], [4, 8, 0, 8]]))

        self.assertIn("LEFT", grid.valid_moves)
        self.assertIn("RIGHT", grid.valid_moves)
        self.assertNotIn("DOWN", grid.valid_moves)
        self.assertNotIn("UP", grid.valid_moves)

    def test_is_game_over(self):
        grid_ok = Game(np.array([[2, 2, 0, 4], [4, 8, 0, 2], [2, 4, 0, 4], [4, 8, 0, 8]]))
        grid_ko = Game(np.array([[2, 4, 2, 4], [4, 8, 4, 2], [2, 4, 8, 4], [4, 8, 2, 8]]))

        self.assertFalse(grid_ok.is_game_over)
        self.assertTrue(grid_ko.is_game_over)
