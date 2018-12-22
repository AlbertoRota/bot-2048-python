from PIL import ImageOps
import pyscreenshot as ImageGrab
import pyautogui
import time

from bot.ai.timed_monte_carlo_ai import TimedMonteCarloAi
from bot.game.board import Board


class Cords:
    cord11, cord12, cord13, cord14 = (170, 350), (280, 350), (280, 350), (500, 350)
    cord21, cord22, cord23, cord24 = (170, 460), (280, 460), (280, 460), (500, 460)
    cord31, cord32, cord33, cord34 = (170, 570), (280, 570), (280, 570), (500, 570)
    cord41, cord42, cord43, cord44 = (170, 680), (280, 680), (280, 680), (500, 680)

    cordArray = [
        [cord11, cord12, cord13, cord14],
        [cord21, cord22, cord23, cord24],
        [cord31, cord32, cord33, cord34],
        [cord41, cord42, cord43, cord44]
    ]


class Values:
    empty = 195
    two = 229
    four = 225
    eight = 190
    sixteen = 172
    thirtyTwo = 157
    sixtyFour = 135
    oneTwentyEight = 205
    twoFiftySix = 201
    fiveOneTwo = 197
    oneZeroTwoFour = 193
    twoZeroFourEight = 189
    fourZeroNineSix = 57

    valueArray = [
        empty, two, four, eight,
        sixteen, thirtyTwo, sixtyFour,
        oneTwentyEight, twoFiftySix,
        fiveOneTwo, oneZeroTwoFour,
        twoZeroFourEight, fourZeroNineSix
    ]


def get_grid():
    image = ImageGrab.grab()
    gray_image = ImageOps.grayscale(image)
    current_grid = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    for row_index, row in enumerate(Cords.cordArray):
        for cell_index, cell in enumerate(row):
            pixel = gray_image.getpixel(cell)
            pos = Values.valueArray.index(pixel)
            if pos == 0:
                current_grid[row_index][cell_index] = 0
            else:
                current_grid[row_index][cell_index] = pow(2, pos)

    return Board(current_grid)


def main():
    board = get_grid()
    while not board.is_game_over:
        direction = TimedMonteCarloAi.get_next_move(board)
        if direction == "UP":
            pyautogui.keyDown("up")
            pyautogui.keyUp("up")
        elif direction == "LEFT":
            pyautogui.keyDown("left")
            pyautogui.keyUp("left")
        elif direction == "RIGHT":
            pyautogui.keyDown("right")
            pyautogui.keyUp("right")
        else:
            pyautogui.keyDown("down")
            pyautogui.keyUp("down")

        time.sleep(0.2)
        board = get_grid()


if __name__ == '__main__':
    main()
