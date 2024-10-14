import pygame
import sys
import random

SCREEN_X = 600
SCREEN_Y = 600

class Snake(object):
    def __init__(self):
        self.dirction = pygame.K_RIGHT
        self.body = []
        for x in range(3):
            self.addnode()

    def addnode(self):
        left, top = (0, 0)
        if self.body:
            left, top = (self.body[0].left, self.body[0].top)
        node = pygame.Rect(left, top, 25, 25)
        if self.dirction == pygame.K_LEFT:
            node.left -= 25
        elif self.dirction == pygame.K_RIGHT:
            node.left += 25
        elif self.dirction == pygame.K_UP:
            node.top -= 25
        elif self.dirction == pygame.K_DOWN:
            node.top += 25
        self.body.insert(0, node)

    def delnode(self):
        self.body.pop()

    def isdead(self):
        if self.body[0].x not in range(SCREEN_X):
            return True
        if self.body[0].y not in range(SCREEN_Y):
            return True
        if self.body[0] in self.body[1:]:
            return True
        return False


    def move(self):
        self.addnode()
        self.delnode()

    def changedirection(self, curkey):
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if curkey in LR + UD:
            if (curkey in LR) and (self.dirction in LR):
                return
            if (curkey in UD) and (self.dirction in UD):
                return
            self.dirction = curkey

class Food:
    def __init__(self):
        self.rect = pygame.Rect(-25, 0, 25, 25)

    def remove(self):
        self.rect.x = -25

    def set(self):
        if self.rect.x == -25:
            allpos = []
            for pos in range(25, SCREEN_X - 25, 25):
                allpos.append(pos)
            self.rect.left = random.choice(allpos)
            self.rect.top = random.choice(allpos)
            print(self.rect)


def show_text(screen, pos, text, color, font_bold=False, font_size=50, font_italic=False):
    cur_font = pygame.font.SysFont("aria label", font_size)
    cur_font.set_bold(font_bold)
    cur_font.set_italic(font_italic)
    text_fmt = cur_font.render(text, 1, color)
    screen.blit(text_fmt, pos)


def begin():
    pygame.init()
    screen_size = (SCREEN_X, SCREEN_Y)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    scores = 0
    isdead = False


    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                snake.changedirection(event.key)
                if event.key == pygame.K_SPACE and isdead:
                    return begin()

        screen.fill((255, 255, 255))

        if not isdead:
            scores += 1
            snake.move()
        for rect in snake.body:
            pygame.draw.rect(screen, (60, 179, 113), rect, 0)

        isdead = snake.isdead()
        if isdead:
            show_text(screen, (100, 200), 'Game Over', (255, 0, 0), False, 100)
            show_text(screen, (160, 270), 'Press space to try again...', (0, 0, 22), False, 30)

        if food.rect == snake.body[0]:
            scores += 50
            food.remove()
            snake.addnode()

        food.set()
        pygame.draw.rect(screen, (0, 0, 255), food.rect, 0)

        show_text(screen, (20, 550), 'Scores: ' + str(scores), (223, 223, 223))

        pygame.display.update()
        clock.tick(10)


if __name__ == '__main__':
    begin()