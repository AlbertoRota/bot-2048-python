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
        board_2048_4x4 = Board2048([
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [2, 4, 0, 0],
            [2, 2, 4, 8]
        ])
        expected_4x4 = {
            Board2048.MOVE_LEFT:    ([
                                         [4, 0, 0, 0],
                                         [0, 0, 0, 0],
                                         [2, 4, 0, 0],
                                         [4, 4, 8, 0]
                                     ], 8),
            Board2048.MOVE_RIGHT:   ([
                                         [0, 0, 0, 4],
                                         [0, 0, 0, 0],
                                         [0, 0, 2, 4],
                                         [0, 4, 4, 8]
                                     ], 8),
            Board2048.MOVE_DOWN:    ([
                                         [0, 0, 0, 0],
                                         [0, 2, 0, 0],
                                         [2, 4, 0, 0],
                                         [4, 2, 4, 8]
                                     ], 4),
            Board2048.MOVE_UP:      ([
                                         [4, 2, 4, 8],
                                         [2, 4, 0, 0],
                                         [0, 2, 0, 0],
                                         [0, 0, 0, 0]
                                     ], 4)
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

        self.assertCountEqual(
            Board2048([
                [2, 2, 0, 4],
                [4, 8, 0, 2],
                [2, 4, 0, 4],
                [4, 8, 0, 8]
            ]).get_moves(),
            [left, right]
        )

        self.assertCountEqual(
            Board2048([
                [2, 4, 2, 0],
                [4, 8, 4, 0],
                [2, 4, 2, 8],
                [4, 8, 4, 2]
            ]).get_moves(),
            [up, right]
        )

        self.assertCountEqual(
            Board2048([
                [0, 2, 0, 4],
                [2, 2, 2, 0],
                [2, 4, 8, 8],
                [0, 2, 0, 4]
            ]).get_moves(),
            [left, right, up, down]
        )

        self.assertCountEqual(
            Board2048([
                [2, 4, 8, 2],
                [2, 4, 8, 2],
                [2, 4, 8, 2],
                [2, 8, 4, 0]
            ]).get_moves(),
            [right, up, down]
        )

        self.assertCountEqual(
            Board2048([
                [0, 2, 4, 8],
                [4, 2, 8, 4],
                [4, 2, 8, 4],
                [4, 2, 8, 4]
            ]).get_moves(),
            [left, up, down]
        )

    def test_is_game_over(self):
        self.assertTrue(
            Board2048([
                [2, 2, 0, 4],
                [4, 8, 0, 2],
                [2, 4, 0, 4],
                [4, 8, 0, 8]
            ]).get_moves()
        )
        self.assertFalse(
            Board2048([
                [2, 4, 2, 4],
                [4, 8, 4, 2],
                [2, 4, 8, 4],
                [4, 8, 2, 8]
            ]).get_moves()
        )
