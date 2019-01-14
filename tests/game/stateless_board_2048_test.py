import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import bot.game.stateless_board_2048 as Board2048


class TestGameMethods(unittest.TestCase):
    def test_swipe_grid(self):
        board_2048_4x4 = [
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [1, 2, 0, 0],
            [1, 1, 2, 3]
        ]
        self.assertEqual(
            Board2048.do_move(board_2048_4x4, Board2048.MOVE_LEFT),
            [
                [2, 0, 0, 0],
                [0, 0, 0, 0],
                [1, 2, 0, 0],
                [2, 2, 3, 0]
            ]
        )
        self.assertEqual(
            Board2048.do_move(board_2048_4x4, Board2048.MOVE_RIGHT),
            [
                [0, 0, 0, 2],
                [0, 0, 0, 0],
                [0, 0, 1, 2],
                [0, 2, 2, 3]
            ]
        )
        self.assertEqual(
            Board2048.do_move(board_2048_4x4, Board2048.MOVE_DOWN),
            [
                [0, 0, 0, 0],
                [0, 1, 0, 0],
                [1, 2, 0, 0],
                [2, 1, 2, 3]
            ]
        )
        self.assertEqual(
            Board2048.do_move(board_2048_4x4, Board2048.MOVE_UP),
            [
                [2, 1, 2, 3],
                [1, 2, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 0]
            ]
        )

    def test_is_valid_move(self):
        left, right, up, down = Board2048.MOVE_LEFT, Board2048.MOVE_RIGHT, Board2048.MOVE_UP, Board2048.MOVE_DOWN

        self.assertCountEqual(
            Board2048.get_moves([
                [2, 2, 0, 4],
                [4, 8, 0, 2],
                [2, 4, 0, 4],
                [4, 8, 0, 8]
            ]),
            [left, right]
        )

        self.assertCountEqual(
            Board2048.get_moves([
                [2, 4, 2, 0],
                [4, 8, 4, 0],
                [2, 4, 2, 8],
                [4, 8, 4, 2]
            ]),
            [up, right]
        )

        self.assertCountEqual(
            Board2048.get_moves([
                [0, 2, 0, 4],
                [2, 2, 2, 0],
                [2, 4, 8, 8],
                [0, 2, 0, 4]
            ]),
            [left, right, up, down]
        )

        self.assertCountEqual(
            Board2048.get_moves([
                [2, 4, 8, 2],
                [2, 4, 8, 2],
                [2, 4, 8, 2],
                [2, 8, 4, 0]
            ]),
            [right, up, down]
        )

        self.assertCountEqual(
            Board2048.get_moves([
                [0, 2, 4, 8],
                [4, 2, 8, 4],
                [4, 2, 8, 4],
                [4, 2, 8, 4]
            ]),
            [left, up, down]
        )

    def test_is_game_over(self):
        self.assertTrue(
            Board2048.get_moves([
                [2, 2, 0, 4],
                [4, 8, 0, 2],
                [2, 4, 0, 4],
                [4, 8, 0, 8]
            ])
        )
        self.assertFalse(
            Board2048.get_moves([
                [2, 4, 2, 4],
                [4, 8, 4, 2],
                [2, 4, 8, 4],
                [4, 8, 2, 8]
            ])
        )
