import pygame
import os
from Card import Card
from Player import Player

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, name, room, uniqueID, hand):
        super(PlayerSprite, self).__init__()
        self.ID = uniqueID
        self.name = name
        self.room = room
        self.surf = pygame.Surface((30, 30))
        self.hand = hand
        self.charImage = None
        myfont = pygame.font.SysFont("monospace", 15)

        if (name == "PLUM"):
            #self.surf.fill((103, 58, 183))
            #self.label = myfont.render("P" + str(uniqueID), 1, (45, 0, 125))
            self.charImage = pygame.image.load(os.path.abspath("images/spr_plum.png"))
        elif (name == "GREEN"):
            #self.surf.fill((76, 175, 80))
            #self.label = myfont.render("P" + str(uniqueID), 1, (6, 95, 10))
            self.charImage = pygame.image.load(os.path.abspath("images/spr_green.png"))
        elif (name == "SCARLET"):
            #self.surf.fill((244, 67, 54))
            #self.label = myfont.render("P" + str(uniqueID), 1, (150, 13, 0))
            self.charImage = pygame.image.load(os.path.abspath("images/spr_scarlet.png"))
        elif (name == "MUSTARD"):
            #self.surf.fill((255, 193, 7))
            #self.label = myfont.render("P" + str(uniqueID), 1, (185, 123, 0))
            self.charImage = pygame.image.load(os.path.abspath("images/spr_mustard.png"))
        elif (name == "WHITE"):
            #self.surf.fill((250, 250, 250))
            #self.label = myfont.render("P" + str(uniqueID), 1, (160, 160, 160))
            self.charImage = pygame.image.load(os.path.abspath("images/spr_white.png"))
        elif (name == "PEACOCK"):
            #self.surf.fill((33, 150, 243))
            #self.label = myfont.render("P" + str(uniqueID), 1, (0, 100, 173))
            self.charImage = pygame.image.load(os.path.abspath("images/spr_peacock.png"))
        self.rect = self.surf.get_rect()
        #self.labelRect = self.label.get_rect()
        self.charImage = pygame.transform.scale(self.charImage, (30, 30))
        self.surf.blit(self.charImage, (0, 0))
        # for initial position only
        self.rect.y = 50 + (36 * uniqueID)
        self.rect.x = 50

    def draw(self, win):
        win.blit(self.surf, self.rect)
        #win.blit(self.label, [self.rect.x + 5, self.rect.y + 6])

    #Getting possible moves, not handling shortcuts right now.
    def get_possible_moves(self):
        if self.room == "H1":
            return [["w","e"],[0,2]]
        elif self.room == "H2":
            return [["w","e"],[2,4]]
        elif self.room == "H6":
            return [["w","e"],[8,10]]
        elif self.room == "H7":
            return [["w","e"],[10,12]]
        elif self.room == "H11":
            return [["w","e"],[16,18]]
        elif self.room == "H12":
            return [["w","e"],[18,20]]
        elif self.room == "H3":
            return [["n","s"],[0,8]]
        elif self.room == "H4":
            return [["n","s"],[2,10]]
        elif self.room == "H5":
            return [["n","s"],[4,12]]
        elif self.room == "H8":
            return [["n","s"],[8,16]]
        elif self.room == "H9":
            return [["n","s"],[10,18]]
        elif self.room == "H10":
            return [["n","s"],[12,20]]
        elif self.room == "STUDY":
            return [["e","s"],[1,5]]
        elif self.room == "HALL":
            return [["e","s","w"],[3,6,1]]
        elif self.room == "LOUNGE":
            return [["w","s"],[3,7]]
        elif self.room == "LIBRARY":
            return [["n","e","s"],[5,9,13]]
        elif self.room == "BILLIARD":
            return [["e","s","w","n"],[11,14,9,6]]
        elif self.room == "DINING":
            return [["w","s","n"],[11,7,15]]
        elif self.room == "CONSERVATORY":
            return [["e","n"],[17,13]]
        elif self.room == "BALL":
            return [["e","n","w"],[19,14,17]]
        elif self.room == "KITCHEN":
            return [["w","n"],[19,15]]

    def create_player_obj(self):
        return Player(self.get_room_num(),self.ID,self.hand)

    def get_room_num(self):
        roomNum = 0
        if self.room == "H1":
            roomNum = 1
        elif self.room == "H2":
            roomNum = 3
        elif self.room == "H6":
            roomNum = 9
        elif self.room == "H7":
            roomNum = 11
        elif self.room == "H11":
            roomNum = 17
        elif self.room == "H12":
            roomNum = 19
        elif self.room == "H3":
            roomNum = 5
        elif self.room == "H4":
            roomNum = 6
        elif self.room == "H5":
            roomNum = 7
        elif self.room == "H8":
            roomNum = 13
        elif self.room == "H9":
            roomNum = 14
        elif self.room == "H10":
            roomNum = 15
        elif self.room == "STUDY":
            roomNum = 0
        elif self.room == "HALL":
            roomNum = 2
        elif self.room == "LOUNGE":
            roomNum = 4
        elif self.room == "LIBRARY":
            roomNum = 8
        elif self.room == "BILLIARD":
            roomNum = 10
        elif self.room == "DINING":
            roomNum = 12
        elif self.room == "CONSERVATORY":
            roomNum = 16
        elif self.room == "BALL":
            roomNum = 18
        elif self.room == "KITCHEN":
            roomNum = 20
        return roomNum
