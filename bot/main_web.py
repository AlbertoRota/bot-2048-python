from PIL import ImageGrab, ImageOps
import pyautogui
import time

from bot.ai.timed_monte_carlo_ai import TimedMonteCarloAi
from bot.game.board import Board


class Cords:
    cord11 = (240, 350)
    cord12 = (355, 350)
    cord13 = (480, 350)
    cord14 = (615, 350)
    cord21 = (240, 475)
    cord22 = (355, 475)
    cord23 = (480, 475)
    cord24 = (615, 475)
    cord31 = (240, 595)
    cord32 = (355, 595)
    cord33 = (480, 595)
    cord34 = (615, 595)
    cord41 = (240, 736)
    cord42 = (355, 736)
    cord43 = (480, 736)
    cord44 = (615, 736)

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

    valueArray = [empty, two, four, eight, sixteen, thirtyTwo, sixtyFour, oneTwentyEight, twoFiftySix, fiveOneTwo, oneZeroTwoFour, twoZeroFourEight, fourZeroNineSix]


def getGrid():
    image = ImageGrab.grab()
    grayImage = ImageOps.grayscale(image)
    currentGrid = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    for row_index, row in enumerate(Cords.cordArray):
        for cell_index, cell in enumerate(row):
            pixel = grayImage.getpixel(cell)
            pos = Values.valueArray.index(pixel)
            if pos == 0:
                currentGrid[row_index][cell_index] = 0
            else:
                currentGrid[row_index][cell_index] = pow(2, pos)

    return Board(currentGrid)


def main():
    board = getGrid()
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

        time.sleep(0.3)
        board = getGrid()


if __name__ == '__main__':
    main()
