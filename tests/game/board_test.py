import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bot.game.board import Board


class TestGameMethods(unittest.TestCase):
    def test_swipe_row_left(self):
        self.assertEqual(Board.__swipe_row_left___([2, 2, 0, 0]), ([4, 0, 0, 0], 4))
        self.assertEqual(Board.__swipe_row_left___([0, 0, 0, 0]), ([0, 0, 0, 0], 0))
        self.assertEqual(Board.__swipe_row_left___([2, 4, 0, 0]), ([2, 4, 0, 0], 0))
        self.assertEqual(Board.__swipe_row_left___([8, 0, 0, 8]), ([16, 0, 0, 0], 16))
        self.assertEqual(Board.__swipe_row_left___([2, 2, 4, 8]), ([4, 4, 8, 0], 4))

    def test_swipe_grid(self):
        board = Board([[2, 2, 0, 0], [0, 0, 0, 0], [2, 4, 0, 0], [2, 2, 4, 8]])
        expected_grid_left = [[4, 0, 0, 0], [0, 0, 0, 0], [2, 4, 0, 0], [4, 4, 8, 0]]
        expected_score_left = 8
        expected_grid_down = [[0, 0, 0, 0], [0, 2, 0, 0], [2, 4, 0, 0], [4, 2, 4, 8]]
        expected_score_down = 4
        expected_grid_right = [[0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 2, 4], [0, 4, 4, 8]]
        expected_score_right = 8
        expected_grid_up = [[4, 2, 4, 8], [2, 4, 0, 0], [0, 2, 0, 0], [0, 0, 0, 0]]
        expected_score_up = 4

        self.assertEqual(board.swipe_grid("LEFT").grid, expected_grid_left)
        self.assertEqual(board.swipe_grid("LEFT").score, expected_score_left)
        self.assertEqual(board.swipe_grid("DOWN").grid, expected_grid_down)
        self.assertEqual(board.swipe_grid("DOWN").score, expected_score_down)
        self.assertEqual(board.swipe_grid("RIGHT").grid, expected_grid_right)
        self.assertEqual(board.swipe_grid("RIGHT").score, expected_score_right)
        self.assertEqual(board.swipe_grid("UP").grid, expected_grid_up)
        self.assertEqual(board.swipe_grid("UP").score, expected_score_up)

    def test_is_valid_move(self):
        board = Board([[2, 2, 0, 4], [4, 8, 0, 2], [2, 4, 0, 4], [4, 8, 0, 8]])
        board_no_up_no_left = Board([[2, 4], [4, 0]])
        board_no_down_no_right = Board([[0, 4], [4, 2]])

        self.assertIn("LEFT", board.valid_moves)
        self.assertIn("RIGHT", board.valid_moves)
        self.assertNotIn("DOWN", board.valid_moves)
        self.assertNotIn("UP", board.valid_moves)

        self.assertNotIn("UP", board_no_up_no_left.valid_moves)
        self.assertNotIn("LEFT", board_no_up_no_left.valid_moves)
        self.assertIn("RIGHT", board_no_up_no_left.valid_moves)
        self.assertIn("DOWN", board_no_up_no_left.valid_moves)

        self.assertIn("UP", board_no_down_no_right.valid_moves)
        self.assertIn("LEFT", board_no_down_no_right.valid_moves)
        self.assertNotIn("RIGHT", board_no_down_no_right.valid_moves)
        self.assertNotIn("DOWN", board_no_down_no_right.valid_moves)

    def test_is_game_over(self):
        grid_ok = Board([[2, 2, 0, 4], [4, 8, 0, 2], [2, 4, 0, 4], [4, 8, 0, 8]])
        grid_ko = Board([[2, 4, 2, 4], [4, 8, 4, 2], [2, 4, 8, 4], [4, 8, 2, 8]])

        self.assertFalse(grid_ok.is_game_over)
        self.assertTrue(grid_ko.is_game_over)
