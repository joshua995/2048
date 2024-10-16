"""
Joshua Liu
October, 2024
2048 Remake
"""

import time
from random import randint

import pygame


class Button(object):
    def __init__(self, x, y, w, h) -> None:
        self.text = pygame.font.SysFont("Arial", h // 2 + h // 4).render(
            "Play Again", True, white
        )
        self.textRect = self.text.get_rect()
        self.textRect.center = (x, y)
        self.w, self.h = self.textRect.width, h
        self.x, self.y = self.textRect.x, self.textRect.y

    def onClick(self, x, y):
        if self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h:
            return True
        return False

    def draw(self):
        pygame.draw.rect(
            screen, green, pygame.Rect(self.x, self.y, self.w, self.h)
        ), screen.blit(self.text, self.textRect)


class Cell(object):
    def __init__(self, pos, value):
        self.pos = [pos[0] + cellSize / 2, pos[1] + cellSize / 2]
        self.value, self.hasChanged = value, False

    def setHasChanged(self, hasChanged):
        self.hasChanged = hasChanged

    def drawCell(self, value):
        stringVal = f"{value}"
        text = pygame.font.SysFont(
            "Arial", cellSize // len(stringVal) + cellSize // len(stringVal) // 4
        ).render(stringVal, True, white)
        textRect = text.get_rect()
        textRect.center = (self.pos[0], self.pos[1])
        screen.blit(text, textRect)


pygame.init()

clock = pygame.time.Clock()

black, white, red, green = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0)

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

score, scorePrefix = 0, "Score :"

playWithNegatives, closeWindow = False, False

playButton = Button(WINDOW_SIZE // 2, WINDOW_SIZE // 2, 150, 75)


def createGrid():
    [
        [
            pygame.draw.rect(
                screen,
                white,
                pygame.Rect(grid[x][y][0], grid[x][y][1], cellSize, cellSize),
                2,
            )
            for y in range(gridSize)
        ]
        for x in range(gridSize)
    ]


getIndexFromPos = lambda pos: [
    (pos[0] - startPos) / cellSize,
    (pos[1] - startPos) / cellSize,
]


# TODO Cause infinite loop when full
def addNewCell():
    global closeWindow
    start = time.time()
    # Pick a random cell that is going to be empty
    randx, randy = randint(0, gridSize - 1), randint(0, gridSize - 1)
    while cellGrid[randx][randy] != None:
        randx, randy = randint(0, gridSize - 1), randint(0, gridSize - 1)
        if time.time() - start > 1:  # Timeout
            closeWindow = True
            break
    randValue = randint(1, 2) * 2  # pick a value 2 or 4 for the new cell
    if playWithNegatives and randint(0, 1) == 0:
        randValue = randint(1, 2) * -2

    cellGrid[randx][randy] = Cell(
        [grid[randx][randy][0], grid[randx][randy][1]], randValue
    )


isMerge = lambda val1, val2: (
    cellGrid[val1[0]][val1[1]] is not None
    and not cellGrid[val1[0]][val1[1]].hasChanged
    and cellGrid[val2[0]][val2[1]] is not None
    and not cellGrid[val2[0]][val2[1]].hasChanged
    and cellGrid[val2[0]][val2[1]].value == cellGrid[val1[0]][val1[1]].value
)


def shiftCells(direction):
    global score
    masterChange = False
    if direction == pygame.K_RIGHT:
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
                                cellGrid[x][y], changed, masterChange = None, True, True
                                break
                for y in range(gridSize):
                    if isMerge([x, y], [x + 1, y]):
                        cellGrid[x + 1][y] = Cell(
                            grid[x + 1][y], cellGrid[x][y].value * 2
                        )
                        score += cellGrid[x][y].value
                        cellGrid[x + 1][y].setHasChanged(True)
                        cellGrid[x][y], changed, masterChange = None, True, True
                        break
    elif direction == pygame.K_LEFT:
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
                                cellGrid[x][y], changed, masterChange = None, True, True
                                break
                for y in range(gridSize):
                    if isMerge([x, y], [x - 1, y]):
                        cellGrid[x - 1][y] = Cell(
                            grid[x - 1][y], cellGrid[x][y].value * 2
                        )
                        score += cellGrid[x][y].value
                        cellGrid[x - 1][y].setHasChanged(True)
                        cellGrid[x][y], changed, masterChange = None, True, True
                        break
    elif direction == pygame.K_UP:
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
                                cellGrid[x][y], changed, masterChange = None, True, True
                                break
                for x in range(gridSize):
                    if isMerge([x, y], [x, y - 1]):
                        cellGrid[x][y - 1] = Cell(
                            grid[x][y - 1], cellGrid[x][y].value * 2
                        )
                        score += cellGrid[x][y].value
                        cellGrid[x][y - 1].setHasChanged(True)
                        cellGrid[x][y], changed, masterChange = None, True, True
                        break
    elif direction == pygame.K_DOWN:
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
                                cellGrid[x][y], changed, masterChange = None, True, True
                                break
                for x in range(gridSize):
                    if isMerge([x, y], [x, y + 1]):
                        cellGrid[x][y + 1] = Cell(
                            grid[x][y + 1], cellGrid[x][y].value * 2
                        )
                        score += cellGrid[x][y].value
                        cellGrid[x][y + 1].setHasChanged(True)
                        cellGrid[x][y], changed, masterChange = None, True, True
                        break
    return masterChange


def isGameOver():
    changed = True
    while changed:
        changed = False
        for x in reversed(range(0, gridSize - 1)):
            for y in range(gridSize):
                if cellGrid[x][y] is not None:
                    for xPlus in range(1, gridSize - x):
                        if cellGrid[x + xPlus][y] is None:
                            return False
            for y in range(gridSize):
                if cellGrid[x][y] is not None:
                    if (
                        cellGrid[x + 1][y] is not None
                        and cellGrid[x + 1][y].value == cellGrid[x][y].value
                    ):
                        return False
    changed = True
    while changed:
        changed = False
        for x in range(1, gridSize):
            for y in range(gridSize):
                if cellGrid[x][y] is not None:
                    for xMin in reversed(range(1, x + 1)):
                        if cellGrid[x - xMin][y] is None:
                            return False
            for y in range(gridSize):
                if cellGrid[x][y] is not None:
                    if (
                        cellGrid[x - 1][y] is not None
                        and cellGrid[x - 1][y].value == cellGrid[x][y].value
                    ):
                        return False
    changed = True
    while changed:
        changed = False
        for y in range(1, gridSize):
            for x in range(gridSize):
                if cellGrid[x][y] is not None:
                    for yMin in reversed(range(1, y + 1)):
                        if cellGrid[x][y - yMin] is None:
                            return False
            for x in range(gridSize):
                if cellGrid[x][y] is not None:
                    if (
                        cellGrid[x][y - 1] is not None
                        and cellGrid[x][y - 1].value == cellGrid[x][y].value
                    ):
                        return False
    changed = True
    while changed:
        changed = False
        for y in reversed(range(0, gridSize - 1)):
            for x in range(gridSize):
                if cellGrid[x][y] is not None:
                    for yPlus in range(1, gridSize - y):
                        if cellGrid[x][y + yPlus] is None:
                            return False
            for x in range(gridSize):
                if cellGrid[x][y] is not None:
                    if (
                        cellGrid[x][y + 1] is not None
                        and cellGrid[x][y + 1].value == cellGrid[x][y].value
                    ):
                        return False
    return True


drawPlayButton = lambda: pygame.draw.rect(
    screen, red, pygame.Rect(WINDOW_SIZE // 2, WINDOW_SIZE // 2, 50, 50)
)


def drawGame():
    screen.fill(black)
    text = FONT_50.render(f"{scorePrefix} {score}", True, white)
    textRect = text.get_rect()
    textRect.midleft = (startPos, startPos - 50)
    screen.blit(text, textRect)
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


def resetGame():
    global grid, cellGrid, score, scorePrefix
    grid = [
        [(startPos + y * cellSize, startPos + x * cellSize) for x in range(gridSize)]
        for y in range(gridSize)
    ]
    cellGrid = [[None for x in range(gridSize)] for y in range(gridSize)]

    score, scorePrefix = 0, "Score: "
    addNewCell(), addNewCell(), drawGame()


if __name__ == "__main__":
    resetGame()
    while not closeWindow:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeWindow = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                (
                    resetGame()
                    if playButton.onClick(mousePos[0], mousePos[1]) and isGameOver
                    else ""
                )
            if event.type == pygame.KEYDOWN:
                addNewCell() if shiftCells(event.key) else ""

        drawGame()
        if isGameOver():
            scorePrefix = "Final Score:"
            playButton.draw()
        clock.tick(60), pygame.display.update()
