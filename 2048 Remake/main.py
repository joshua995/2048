"""
Joshua Liu
October 9th, 2024
2048 Remake
"""

import time
from random import randint

import pygame


class Cell(object):
    def __init__(self, pos, value):
        self.pos = [pos[0] + cellSize / 2, pos[1] + cellSize / 2]
        self.value = value
        self.hasChanged = False

    def setHasChanged(self, hasChanged):
        self.hasChanged = hasChanged

    def drawCell(self, value):
        stringVal = f"{value}"
        text = pygame.font.SysFont(
            "Arial", cellSize // len(stringVal) + cellSize // len(stringVal) // 4
        ).render(stringVal, True, white)
        text_rect = text.get_rect()
        text_rect.center = (self.pos[0], self.pos[1])
        screen.blit(text, text_rect)


pygame.init()

clock = pygame.time.Clock()

black, white, red, green, lightBlue = (
    (0, 0, 0),
    (255, 255, 255),
    (255, 0, 0),
    (0, 255, 0),
    (0, 100, 255),
)
yellow = (255, 255, 0)

WINDOW_SIZE = 750  # WINDOW_SIZE default 750
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("2048"), screen.fill(black)

gridSize = 4
cellSize = int(WINDOW_SIZE // (gridSize * 1.25))

FONT_50 = pygame.font.SysFont("Arial", int(50))

startPos = (WINDOW_SIZE - (gridSize * cellSize)) / 2  # Starting pos to center the board

# x, y
grid = [
    [(startPos + y * cellSize, startPos + x * cellSize) for x in range(gridSize)]
    for y in range(gridSize)
]

cellGrid = [[None for x in range(gridSize)] for y in range(gridSize)]

score = 0
scorePrefix = "Score :"

playWithNegatives = False

closeWindow = False


def createGrid():
    for x in range(gridSize):
        for y in range(gridSize):
            pygame.draw.rect(
                screen,
                white,
                pygame.Rect(grid[x][y][0], grid[x][y][1], cellSize, cellSize),
                2,
            )


def getIndexFromPos(pos):
    return [(pos[0] - startPos) / cellSize, (pos[1] - startPos) / cellSize]


# TODO Cause infinite loop when full
def addNewCell():
    global closeWindow
    start = time.time()
    # Pick a random cell that is going to be empty
    randx = randint(0, gridSize - 1)
    randy = randint(0, gridSize - 1)
    while cellGrid[randx][randy] != None:
        randx = randint(0, gridSize - 1)
        randy = randint(0, gridSize - 1)
        if time.time() - start > 1:  # Timeout
            closeWindow = True
            break
    randValue = randint(1, 2) * 2  # pick a value 2 or 4 for the new cell
    if playWithNegatives and randint(0, 1) == 0:
        randValue = randint(1, 2) * -2
    # generate the new cell
    tempC = Cell([grid[randx][randy][0], grid[randx][randy][1]], randValue)
    cellGrid[randx][randy] = tempC


def shiftCells(direction):
    global score
    masterChange = False
    if direction == "r":
        changed = True
        while changed:
            changed = False
            for x in reversed(range(0, gridSize - 1)):
                for y in range(gridSize):
                    if cellGrid[x][y] is not None:
                        for xPlus in range(1, gridSize - x):
                            if cellGrid[x + xPlus][y] is None:
                                cellGrid[x + xPlus][y] = Cell(
                                    grid[x + xPlus][y], cellGrid[x][y].value
                                )
                                cellGrid[x][y] = None
                                changed = True
                                masterChange = True
                                break
                for y in range(gridSize):
                    if cellGrid[x][y] is not None and not cellGrid[x][y].hasChanged:
                        if (
                            cellGrid[x + 1][y] is not None
                            and not cellGrid[x + 1][y].hasChanged
                            and cellGrid[x + 1][y].value == cellGrid[x][y].value
                        ):
                            cellGrid[x + 1][y] = Cell(
                                grid[x + 1][y], cellGrid[x][y].value * 2
                            )
                            score += cellGrid[x][y].value
                            cellGrid[x + 1][y].setHasChanged(True)
                            cellGrid[x][y] = None
                            changed = True
                            masterChange = True
                            break
    elif direction == "l":
        changed = True
        while changed:
            changed = False
            for x in range(1, gridSize):
                for y in range(gridSize):
                    if cellGrid[x][y] is not None:
                        for xMin in reversed(range(1, x + 1)):
                            if cellGrid[x - xMin][y] is None:
                                cellGrid[x - xMin][y] = Cell(
                                    grid[x - xMin][y], cellGrid[x][y].value
                                )
                                cellGrid[x][y] = None
                                changed = True
                                masterChange = True
                                break
                for y in range(gridSize):
                    if cellGrid[x][y] is not None and not cellGrid[x][y].hasChanged:
                        if (
                            cellGrid[x - 1][y] is not None
                            and not cellGrid[x - 1][y].hasChanged
                            and cellGrid[x - 1][y].value == cellGrid[x][y].value
                        ):
                            cellGrid[x - 1][y] = Cell(
                                grid[x - 1][y], cellGrid[x][y].value * 2
                            )
                            score += cellGrid[x][y].value
                            cellGrid[x - 1][y].setHasChanged(True)
                            cellGrid[x][y] = None
                            changed = True
                            masterChange = True
                            break
    elif direction == "u":
        changed = True
        while changed:
            changed = False
            for y in range(1, gridSize):
                for x in range(gridSize):
                    if cellGrid[x][y] is not None:
                        for yMin in reversed(range(1, y + 1)):
                            if cellGrid[x][y - yMin] is None:
                                cellGrid[x][y - yMin] = Cell(
                                    grid[x][y - yMin], cellGrid[x][y].value
                                )
                                cellGrid[x][y] = None
                                changed = True
                                masterChange = True
                                break
                for x in range(gridSize):
                    if cellGrid[x][y] is not None and not cellGrid[x][y].hasChanged:
                        if (
                            cellGrid[x][y - 1] is not None
                            and not cellGrid[x][y - 1].hasChanged
                            and cellGrid[x][y - 1].value == cellGrid[x][y].value
                        ):
                            cellGrid[x][y - 1] = Cell(
                                grid[x][y - 1], cellGrid[x][y].value * 2
                            )
                            score += cellGrid[x][y].value
                            cellGrid[x][y - 1].setHasChanged(True)
                            cellGrid[x][y] = None
                            changed = True
                            masterChange = True
                            break
    else:
        changed = True
        while changed:
            changed = False
            for y in reversed(range(0, gridSize - 1)):
                for x in range(gridSize):
                    if cellGrid[x][y] is not None:
                        for yPlus in range(1, gridSize - y):
                            if cellGrid[x][y + yPlus] is None:
                                cellGrid[x][y + yPlus] = Cell(
                                    grid[x][y + yPlus], cellGrid[x][y].value
                                )
                                cellGrid[x][y] = None
                                changed = True
                                masterChange = True
                                break
                for x in range(gridSize):
                    if cellGrid[x][y] is not None and not cellGrid[x][y].hasChanged:
                        if (
                            cellGrid[x][y + 1] is not None
                            and not cellGrid[x][y + 1].hasChanged
                            and cellGrid[x][y + 1].value == cellGrid[x][y].value
                        ):
                            cellGrid[x][y + 1] = Cell(
                                grid[x][y + 1], cellGrid[x][y].value * 2
                            )
                            score += cellGrid[x][y].value
                            cellGrid[x][y + 1].setHasChanged(True)
                            cellGrid[x][y] = None
                            changed = True
                            masterChange = True
                            break
    return masterChange


def isGameOver():
    global score
    masterChange = False
    changed = True
    while changed:
        changed = False
        for x in reversed(range(0, gridSize - 1)):
            for y in range(gridSize):
                if cellGrid[x][y] is not None:
                    for xPlus in range(1, gridSize - x):
                        if cellGrid[x + xPlus][y] is None:
                            masterChange = True
                            break
            for y in range(gridSize):
                if cellGrid[x][y] is not None:
                    if (
                        cellGrid[x + 1][y] is not None
                        and cellGrid[x + 1][y].value == cellGrid[x][y].value
                    ):
                        masterChange = True
                        break
    changed = True
    while changed:
        changed = False
        for x in range(1, gridSize):
            for y in range(gridSize):
                if cellGrid[x][y] is not None:
                    for xMin in reversed(range(1, x + 1)):
                        if cellGrid[x - xMin][y] is None:
                            masterChange = True
                            break
            for y in range(gridSize):
                if cellGrid[x][y] is not None :
                    if (
                        cellGrid[x - 1][y] is not None
                        and cellGrid[x - 1][y].value == cellGrid[x][y].value
                    ):
                        masterChange = True
                        break
    changed = True
    while changed:
        changed = False
        for y in range(1, gridSize):
            for x in range(gridSize):
                if cellGrid[x][y] is not None:
                    for yMin in reversed(range(1, y + 1)):
                        if cellGrid[x][y - yMin] is None:
                            masterChange = True
                            break
            for x in range(gridSize):
                if cellGrid[x][y] is not None :
                    if (
                        cellGrid[x][y - 1] is not None
                        and cellGrid[x][y - 1].value == cellGrid[x][y].value
                    ):
                        masterChange = True
                        break
    changed = True
    while changed:
        changed = False
        for y in reversed(range(0, gridSize - 1)):
            for x in range(gridSize):
                if cellGrid[x][y] is not None:
                    for yPlus in range(1, gridSize - y):
                        if cellGrid[x][y + yPlus] is None:
                            masterChange = True
                            break
            for x in range(gridSize):
                if cellGrid[x][y] is not None :
                    if (
                        cellGrid[x][y + 1] is not None
                        and cellGrid[x][y + 1].value == cellGrid[x][y].value
                    ):
                        masterChange = True
                        break
    return not masterChange


def drawGame():
    screen.fill(black)
    text = FONT_50.render(f"{scorePrefix} {score}", True, white)
    text_rect = text.get_rect()
    text_rect.midleft = (startPos, startPos - 50)
    screen.blit(text, text_rect)
    createGrid()
    [
        [
            (
                cellGrid[x][y].drawCell(cellGrid[x][y].value),
                cellGrid[x][y].setHasChanged(False),
            )
            for y in range(gridSize)
            if cellGrid[x][y] is not None
        ]
        for x in range(gridSize)
    ]


if __name__ == "__main__":
    addNewCell()
    addNewCell()
    drawGame()
    while not closeWindow:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeWindow = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
            if (
                event.type == pygame.KEYDOWN
            ):  # TODO not quite right. Missing check no change
                if event.key == pygame.K_RIGHT:
                    if shiftCells("r"):
                        addNewCell()
                        if isGameOver():
                            scorePrefix = "Final Score:"
                        drawGame()
                if event.key == pygame.K_LEFT:
                    if shiftCells("l"):
                        addNewCell()
                        if isGameOver():
                            scorePrefix = "Final Score:"
                        drawGame()
                if event.key == pygame.K_UP:
                    if shiftCells("u"):
                        addNewCell()
                        if isGameOver():
                            scorePrefix = "Final Score:"
                        drawGame()
                if event.key == pygame.K_DOWN:
                    if shiftCells("d"):
                        addNewCell()
                        if isGameOver():
                            scorePrefix = "Final Score:"
                        drawGame()
        clock.tick(60)
        pygame.display.update()
