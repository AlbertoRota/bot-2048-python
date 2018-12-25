import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from bot.game.board_2048 import Board2048


class TestGameMethods(unittest.TestCase):
    def test_swipe_row_left(self):
        self.assertEqual(
            Board2048.swipe_row_left([2, 2, 0, 0]),
            ([4, 0, 0, 0], 4)
        )
        self.assertEqual(
            Board2048.swipe_row_left([0, 0, 0, 0]),
            ([0, 0, 0, 0], 0)
        )
        self.assertEqual(Board2048.swipe_row_left(
            [2, 4, 0, 0]),
            ([2, 4, 0, 0], 0)
        )
        self.assertEqual(
            Board2048.swipe_row_left([8, 0, 0, 8]),
            ([16, 0, 0, 0], 16)
        )
        self.assertEqual(
            Board2048.swipe_row_left([2, 2, 4, 8]),
            ([4, 4, 8, 0], 4)
        )

    def test_swipe_grid(self):
        board_2048_3x3 = Board2048([[2, 2, 0], [0, 0, 0], [2, 4, 0]])
        expected_3x3 = {
            Board2048.MOVE_LEFT:    ([[4, 0, 0], [0, 0, 0], [2, 4, 0]], 4),
            Board2048.MOVE_RIGHT:   ([[0, 0, 4], [0, 0, 0], [0, 2, 4]], 4),
            Board2048.MOVE_DOWN:    ([[0, 0, 0], [0, 2, 0], [4, 4, 0]], 4),
            Board2048.MOVE_UP:      ([[4, 2, 0], [0, 4, 0], [0, 0, 0]], 4)
        }
        self.__check_moves__(board_2048_3x3, expected_3x3)

        board_2048_4x4 = Board2048([[2, 2, 0, 0], [0, 0, 0, 0], [2, 4, 0, 0], [2, 2, 4, 8]])
        expected_4x4 = {
            Board2048.MOVE_LEFT:    ([[4, 0, 0, 0], [0, 0, 0, 0], [2, 4, 0, 0], [4, 4, 8, 0]], 8),
            Board2048.MOVE_RIGHT:   ([[0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 2, 4], [0, 4, 4, 8]], 8),
            Board2048.MOVE_DOWN:    ([[0, 0, 0, 0], [0, 2, 0, 0], [2, 4, 0, 0], [4, 2, 4, 8]], 4),
            Board2048.MOVE_UP:      ([[4, 2, 4, 8], [2, 4, 0, 0], [0, 2, 0, 0], [0, 0, 0, 0]], 4)
        }
        self.__check_moves__(board_2048_4x4, expected_4x4)

    def __check_moves__(self, board_2048, expected):
        for move, expected_results in expected.items():
            board_to_move = board_2048.clone()
            board_to_move.do_move(move, False)
            self.assertEqual(board_to_move.grid, expected_results[0])
            self.assertEqual(board_to_move.score, expected_results[1])
            self.assertEqual(board_to_move.get_result(), expected_results[1])

    def test_is_valid_move(self):
        left, right, up, down = Board2048.MOVE_LEFT, Board2048.MOVE_RIGHT, Board2048.MOVE_UP, Board2048.MOVE_DOWN

        board_2048_4x4_left_right = Board2048([[2, 2, 0, 4], [4, 8, 0, 2], [2, 4, 0, 4], [4, 8, 0, 8]])
        self.assertCountEqual(board_2048_4x4_left_right.get_moves(), [left, right])

        board_2048_3x3_up_right = Board2048([[2, 4, 0], [4, 8, 0], [2, 4, 2]])
        self.assertCountEqual(board_2048_3x3_up_right.get_moves(), [up, right])

        board_2048_3x3_all = Board2048([[0, 2, 0], [2, 2, 2], [2, 4, 8]])
        self.assertCountEqual(board_2048_3x3_all.get_moves(), [left, right, up, down])

        board_2048_2x2_no_left = Board2048([[2, 4], [2, 0]])
        self.assertCountEqual(board_2048_2x2_no_left.get_moves(), [right, up, down])

        board_2048_2x2_no_right = Board2048([[0, 2], [4, 2]])
        self.assertCountEqual(board_2048_2x2_no_right.get_moves(), [left, up, down])

    def test_is_game_over(self):
        board_2048_ok = Board2048([[2, 2, 0, 4], [4, 8, 0, 2], [2, 4, 0, 4], [4, 8, 0, 8]])
        board_2048_ko = Board2048([[2, 4, 2, 4], [4, 8, 4, 2], [2, 4, 8, 4], [4, 8, 2, 8]])

        self.assertTrue(board_2048_ok.get_moves())
        self.assertFalse(board_2048_ko.get_moves())
