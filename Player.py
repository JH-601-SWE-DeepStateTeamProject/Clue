import pygame
from Card import Card
from Map import Map


class Player():
    def __init__(self, x, y, width, height, color, hand):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 100
        self.hand = []
        for card in hand:
            self.hand.append(Card(card))

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        moved = False
        keys = pygame.key.get_pressed()
        tempPos = [self.y, self.x]

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.x - self.vel < 0:
                return moved
            self.x -= self.vel
            moved = True

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.x + self.vel >= 500:
                return moved
            self.x += self.vel
            moved = True

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.y - self.vel < 0:
                return moved
            self.y -= self.vel
            moved = True

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.y + self.vel >= 500:
                return moved
            self.y += self.vel
            moved = True

        # Checks if move was to an invalid room and negates the move if so
        if self.get_room() == "":
            moved = False
            self.y = tempPos[0]
            self.x = tempPos[1]

        self.update()
        return moved

    def get_room(self):
        map = Map().map
        return map[int(self.y / 100)][int(self.x / 100)]

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
