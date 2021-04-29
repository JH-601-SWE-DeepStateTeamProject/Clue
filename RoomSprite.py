import os
import pygame
import math
import os

class RoomSprite(pygame.sprite.Sprite):
    def __init__(self, name):
        super(RoomSprite, self).__init__()
        self.name = name
        self.playersInRoom = []
        self.label = None
        self.roomImage = None
        myfont = pygame.font.SysFont("monospace", 15)

        if (name == "STUDY"):
            self.surf = pygame.Surface((120, 120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 140
            self.rect.y = 40
            self.roomType = "ROOM"
        elif (name == "TUNNEL1"):
            self.surf = pygame.Surface((40, 40))
            self.surf.fill((207, 216, 220))
            self.rect = self.surf.get_rect()
            self.rect.x = 220
            self.rect.y = 120
            self.roomType = "TUNNEL"
        elif (name == "H1"):
            self.surf = pygame.Surface((80, 40))
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 260
            self.rect.y = 80
            self.roomType = "H_HALL"
        elif (name == "HALL"):
            self.surf = pygame.Surface((120, 120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 340
            self.rect.y = 40
            self.roomType = "ROOM"
        elif (name == "H2"):
            self.surf = pygame.Surface((80, 40))
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 460
            self.rect.y = 80
            self.roomType = "H_HALL"
        elif (name == "LOUNGE"):
            self.surf = pygame.Surface((120, 120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 540
            self.rect.y = 40
            self.roomType = "ROOM"
        elif (name == "TUNNEL2"):
            self.surf = pygame.Surface((40, 40))
            self.surf.fill((207, 216, 220))
            self.rect = self.surf.get_rect()
            self.rect.x = 540
            self.rect.y = 120
            self.roomType = "TUNNEL"
        elif (name == "H3"):
            self.surf = pygame.Surface((40, 80))
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 180
            self.rect.y = 160
            self.roomType = "V_HALL"
        elif (name == "H4"):
            self.surf = pygame.Surface((40, 80))
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 380
            self.rect.y = 160
            self.roomType = "V_HALL"
        elif (name == "H5"):
            self.surf = pygame.Surface((40, 80))
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 580
            self.rect.y = 160
            self.roomType = "V_HALL"
        elif (name == "LIBRARY"):
            self.surf = pygame.Surface((120, 120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 140
            self.rect.y = 240
            self.roomType = "ROOM"
        elif (name == "H6"):
            self.surf = pygame.Surface((80, 40))
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 260
            self.rect.y = 280
            self.roomType = "H_HALL"
        elif (name == "BILLIARD"):
            self.surf = pygame.Surface((120, 120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 340
            self.rect.y = 240
            self.roomType = "ROOM"
        elif (name == "H7"):
            self.surf = pygame.Surface((80, 40))
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 460
            self.rect.y = 280
            self.roomType = "H_HALL"
        elif (name == "DINING"):
            self.surf = pygame.Surface((120, 120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 540
            self.rect.y = 240
            self.roomType = "ROOM"
        elif (name == "H8"):
            self.surf = pygame.Surface((40, 80))
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 180
            self.rect.y = 360
            self.roomType = "V_HALL"
        elif (name == "H9"):
            self.surf = pygame.Surface((40, 80))
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 380
            self.rect.y = 360
            self.roomType = "V_HALL"
        elif (name == "H10"):
            self.surf = pygame.Surface((40, 80))
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 580
            self.rect.y = 360
            self.roomType = "V_HALL"
        elif (name == "CONSERVATORY"):
            self.surf = pygame.Surface((120, 120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 140
            self.rect.y = 440
            self.roomType = "ROOM"
        elif (name == "TUNNEL3"):
            self.surf = pygame.Surface((40, 40))
            self.surf.fill((207, 216, 220))
            self.rect = self.surf.get_rect()
            self.rect.x = 220
            self.rect.y = 440
            self.roomType = "TUNNEL"
        elif (name == "H11"):
            self.surf = pygame.Surface((80, 40))
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 260
            self.rect.y = 480
            self.roomType = "H_HALL"
        elif (name == "BALL"):
            self.surf = pygame.Surface((120, 120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 340
            self.rect.y = 440
            self.roomType = "ROOM"
        elif (name == "H12"):
            self.surf = pygame.Surface((80, 40))
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 460
            self.rect.y = 480
            self.roomType = "H_HALL"
        elif (name == "KITCHEN"):
            self.surf = pygame.Surface((120, 120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 540
            self.rect.y = 440
            self.roomType = "ROOM"
        elif (name == "TUNNEL4"):
            self.surf = pygame.Surface((40, 40))
            self.surf.fill((207, 216, 220))
            self.rect = self.surf.get_rect()
            self.rect.x = 540
            self.rect.y = 440
            self.roomType = "TUNNEL"

        if (self.roomType == "ROOM"):
            self.roomImage = pygame.image.load(os.path.abspath("images/room.png"))
            self.roomImage = pygame.transform.scale(self.roomImage, (120,120))
            self.label = myfont.render(name.capitalize(), 1, (69, 90, 100))
        elif (self.roomType == "TUNNEL"):
            if (int(self.name[-1]) % 2) == 0:
                self.roomImage = pygame.image.load(os.path.abspath("images/tunnel_left.png"))
            else:
                self.roomImage = pygame.image.load(os.path.abspath("images/tunnel_right.png"))
            self.roomImage = pygame.transform.scale(self.roomImage, (40,40))
        elif (self.roomType == "H_HALL"):
            self.roomImage = pygame.image.load(os.path.abspath("images/hall_h.png"))
            self.roomImage = pygame.transform.scale(self.roomImage, (80,40))
        elif (self.roomType == "V_HALL"):
            self.roomImage = pygame.image.load(os.path.abspath("images/hall_v.png"))
            self.roomImage = pygame.transform.scale(self.roomImage, (40,80))
        self.surf.blit(self.roomImage, (0, 0))

    # gives a position to players moving to this room
    def openPlacement(self):
        if (self.roomType == "TUNNEL"):
            return [self.rect.x + 5, self.rect.y + 5]
        elif (self.roomType == "V_HALL"):
            return [self.rect.x + 5, self.rect.y + 25]
        elif (self.roomType == "H_HALL"):
            return [self.rect.x + 25, self.rect.y + 5]
        elif (self.roomType == "ROOM"):
            oc = len(self.playersInRoom)
        return [self.rect.x + 5 + ((oc % 3) * 40), self.rect.y + 5 + ((math.floor(oc / 3)) * 40)]

    def draw(self, win):
        win.blit(self.surf, self.rect)
        if (self.label != None):
            win.blit(self.label, [self.rect.x + (self.rect.width / 2) - (self.label.get_width() / 2), self.rect.y + (self.rect.width / 2) - (self.label.get_height() / 2)])
