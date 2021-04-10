#this will need to be incorporated to client.py - only want a single game loop, client side
import pygame
import math
pygame.init()
myfont = pygame.font.SysFont("monospace", 15)

class ClueBoard:
    #clueboard contains all players, room, and cards
    Players = []
    Rooms = []
    Cards = [] # not yet implemented
    
    def initialize(self, PlayerData):
        #initialize rooms. hardcoded because the rooms do not change
        #tunnels also handled as room objects for now - this implementation may need to be changed in future
        self.Rooms.extend(
            [RoomSprite("STUDY"), RoomSprite("H1"), RoomSprite("HALL"), RoomSprite("H2"), RoomSprite("LOUNGE"),
             RoomSprite("H3"), RoomSprite("H4"), RoomSprite("H5"),
             RoomSprite("LIBRARY"), RoomSprite("H6"), RoomSprite("BILLIARD"), RoomSprite("H7"), RoomSprite("DINING"),
             RoomSprite("H8"), RoomSprite("H9"), RoomSprite("H10"),
             RoomSprite("CONSERVATORY"), RoomSprite("H11"), RoomSprite("BALL"), RoomSprite("H12"), RoomSprite("KITCHEN"),
             RoomSprite("TUNNEL1"), RoomSprite("TUNNEL2"), RoomSprite("TUNNEL3"),RoomSprite("TUNNEL4")
        ])
        #initialize player data. need to use initialization data from server to set up
        #hard-coded for now. need to tie specific players to their unique client id as provided by server. unique id is 3rd parameter
        p1 = PlayerSprite("SCARLET", "INITIAL", 1)
        self.Players.append(p1)
        p2 = PlayerSprite("MUSTARD", "INITIAL", 2)
        self.Players.append(p2)
        p3 = PlayerSprite("GREEN", "INITIAL", 3)
        self.Players.append(p3)
        p4 = PlayerSprite("PEACOCK", "INITIAL", 4)
        self.Players.append(p4)
        p5 = PlayerSprite("PLUM", "INITIAL", 5)
        self.Players.append(p5)
        p6 = PlayerSprite("WHITE", "INITIAL", 6)
        self.Players.append(p6)

    #pass in room and player to update
    def movePlayerInstance(self, characterObj, newRoomObj):
        #checks if player is already in the room. this kind of move shouldn't be allowed by back end logic
        if (characterObj.room == newRoomObj.name):
            pass
        else:
            #remove player from old room, append to new room, and update the current room for the player. pass in objects for the player and each room
            #move player sprite to correct room
            if characterObj.room == "INITIAL":
                characterObj.room = ""
            else: 
                #remove the player from their old room
                #iterate through rooms
                for room in self.Rooms:
                    if characterObj.room == room.name:
                        #match on room name. iterate through the player list that the room has
                        for pl in room.playersInRoom:
                            #match on player name
                            if (pl.name == characterObj.name):
                                room.playersInRoom.remove(pl)
                
            #update the players rect, update their current room. add the player object to that rooms player list
            newPos = newRoomObj.openPlacement()
            characterObj.rect.x = newPos[0]
            characterObj.rect.y = newPos[1]
            characterObj.room = newRoomObj.name
            newRoomObj.playersInRoom.append(characterObj)
            
    def draw(self, window):
        for room in self.Rooms:
            room.draw(window)
        for player in self.Players:
            player.draw(window)



#global var to store the gameboard
Board = ClueBoard()

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, name, room, uniqueID):
        super(PlayerSprite, self).__init__()
        self.ID = uniqueID
        self.name = name  
        self.room = room

        self.surf = pygame.Surface((30,30))
        if (name == "PLUM"):
            self.surf.fill((103, 58, 183))
            self.label = myfont.render("P" + str(uniqueID), 1, (45,0,125))
        elif (name == "GREEN"):
            self.surf.fill((76, 175, 80))
            self.label = myfont.render("P" + str(uniqueID), 1, (6, 95, 10))
        elif (name == "SCARLET"):
            self.surf.fill((244, 67, 54))
            self.label = myfont.render("P" + str(uniqueID), 1, (150, 13, 0))
        elif (name == "MUSTARD"):
            self.surf.fill((255, 193, 7))
            self.label = myfont.render("P" + str(uniqueID), 1, (185, 123, 0))
        elif (name == "WHITE"):
            self.surf.fill((250, 250, 250))
            self.label = myfont.render("P" + str(uniqueID), 1, (160,160,160))
        elif (name == "PEACOCK"):
            self.surf.fill((33, 150, 243))
            self.label = myfont.render("P" + str(uniqueID), 1, (0,100,173))
        self.rect = self.surf.get_rect()
        self.labelRect = self.label.get_rect()
        
        #for initial position only
        self.rect.y = 50 + (36 * len(Board.Players))
        self.rect.x = 50
    
    def draw(self, win):
        win.blit(self.surf, self.rect)
        win.blit(self.label, [self.rect.x + 5, self.rect.y + 6])
    
    
class RoomSprite(pygame.sprite.Sprite):
    def __init__(self, name):
        super(RoomSprite, self).__init__()
        self.name = name
        self.playersInRoom = []
        self.label = None
        if (name == "STUDY"):
            self.surf = pygame.Surface((120,120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 140
            self.rect.y = 40
            self.roomType = "ROOM"
        elif (name == "TUNNEL1"):
            self.surf = pygame.Surface((40,40))
            self.surf.fill((207, 216,220))
            self.rect = self.surf.get_rect()
            self.rect.x = 220
            self.rect.y = 120
            self.roomType = "TUNNEL"
        elif (name == "H1"):
            self.surf = pygame.Surface((80,40))    
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 260
            self.rect.y = 80
            self.roomType = "H_HALL"
        elif (name == "HALL"):
            self.surf = pygame.Surface((120,120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 340
            self.rect.y = 40
            self.roomType = "ROOM"
        elif (name == "H2"):
            self.surf = pygame.Surface((80,40))    
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 460
            self.rect.y = 80
            self.roomType = "H_HALL"
        elif (name == "LOUNGE"):
            self.surf = pygame.Surface((120,120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 540
            self.rect.y = 40
            self.roomType = "ROOM"
        elif (name == "TUNNEL2"):
            self.surf = pygame.Surface((40,40))
            self.surf.fill((207, 216,220))
            self.rect = self.surf.get_rect()
            self.rect.x = 540
            self.rect.y = 120
            self.roomType = "TUNNEL"
        elif (name == "H3"):
            self.surf = pygame.Surface((40,80))    
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 180
            self.rect.y = 160
            self.roomType = "V_HALL"
        elif (name == "H4"):
            self.surf = pygame.Surface((40,80))    
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 380
            self.rect.y = 160
            self.roomType = "V_HALL"
        elif (name == "H5"):
            self.surf = pygame.Surface((40,80))    
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 580
            self.rect.y = 160
            self.roomType = "V_HALL"
        elif (name == "LIBRARY"):
            self.surf = pygame.Surface((120,120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 140
            self.rect.y = 240
            self.roomType = "ROOM"
        elif (name == "H6"):
            self.surf = pygame.Surface((80,40))    
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 260
            self.rect.y = 280
            self.roomType = "H_HALL"
        elif (name == "BILLIARD"):
            self.surf = pygame.Surface((120,120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 340
            self.rect.y = 240
            self.roomType = "ROOM"
        elif (name == "H7"):
            self.surf = pygame.Surface((80,40))    
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 460
            self.rect.y = 280
            self.roomType = "H_HALL"
        elif (name == "DINING"):
            self.surf = pygame.Surface((120,120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 540
            self.rect.y = 240
            self.roomType = "ROOM"
        elif (name == "H8"):
            self.surf = pygame.Surface((40,80))    
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 180
            self.rect.y = 360
            self.roomType = "V_HALL"
        elif (name == "H9"):
            self.surf = pygame.Surface((40,80))    
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 380
            self.rect.y = 360
            self.roomType = "V_HALL"
        elif (name == "H10"):
            self.surf = pygame.Surface((40,80))    
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 580
            self.rect.y = 360
            self.roomType = "V_HALL"
        elif (name == "CONSERVATORY"):
            self.surf = pygame.Surface((120,120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 140
            self.rect.y = 440
            self.roomType = "ROOM"
        elif (name == "TUNNEL3"):
            self.surf = pygame.Surface((40,40))
            self.surf.fill((207, 216,220))
            self.rect = self.surf.get_rect()
            self.rect.x = 220
            self.rect.y = 440
            self.roomType = "TUNNEL"
        elif (name == "H11"):
            self.surf = pygame.Surface((80,40))    
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 260
            self.rect.y = 480
            self.roomType = "H_HALL"
        elif (name == "BALL"):
            self.surf = pygame.Surface((120,120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 340
            self.rect.y = 440
            self.roomType = "ROOM"
        elif (name == "H12"):
            self.surf = pygame.Surface((80,40))    
            self.surf.fill((96, 125, 139))
            self.rect = self.surf.get_rect()
            self.rect.x = 460
            self.rect.y = 480
            self.roomType = "H_HALL"
        elif (name == "KITCHEN"):
            self.surf = pygame.Surface((120,120))
            self.surf.fill((147, 167, 177))
            self.rect = self.surf.get_rect()
            self.rect.x = 540
            self.rect.y = 440
            self.roomType = "ROOM"
        elif (name == "TUNNEL4"):
            self.surf = pygame.Surface((40,40))
            self.surf.fill((207, 216,220))
            self.rect = self.surf.get_rect()
            self.rect.x = 540
            self.rect.y = 440
            self.roomType = "TUNNEL"
            
        if (self.roomType == "ROOM"):
            self.label = myfont.render(name.capitalize(), 1, (69, 90, 100))
    #gives a position to players moving to this room
    def openPlacement(self):
        if (self.roomType == "TUNNEL"):
            return [self.rect.x + 5, self.rect.y + 5]
        elif (self.roomType == "V_HALL"):
            return [self.rect.x + 5, self.rect.y + 25]
        elif (self.roomType == "H_HALL"):
            return [self.rect.x + 25, self.rect.y + 5]
        elif (self.roomType == "ROOM"):
            oc = len(self.playersInRoom)
            return [self.rect.x + 5 + ((oc % 3) * 40), self.rect.y + 5 + ( (math.floor(oc / 3))* 40)]
        
    def draw(self, win):
        win.blit(self.surf, self.rect)
        if (self.label != None):
            win.blit(self.label, [self.rect.x + (self.rect.width / 2) - (self.label.get_width() / 2), self.rect.y + (self.rect.width / 2) - (self.label.get_height() / 2)])

#this needs to be called from server. used to initialize game objects - players, cards, turn, etc
def initialize(PlayerData):
    #initialize the board. pass in the player data from the server
    Board.initialize(PlayerData)
    #other initialization outside of board obj that we may need can go here
    #call main to start the game loop
    main()
    pass

def main():
    #initialize the window, then run game loop
    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Clueless Game")
    running = True
    
    # here's a method to move players. if needed I can change this so
    # that we can move players using either character name or by client unique id. currently uses the direct instance of a player
    # rooms will need an update method implemented to acccount for adjusting positions after a player leaves
    Board.movePlayerInstance(Board.Players[0], Board.Rooms[0])
    Board.movePlayerInstance(Board.Players[1], Board.Rooms[2])
    Board.movePlayerInstance(Board.Players[2], Board.Rooms[4])
    Board.movePlayerInstance(Board.Players[3], Board.Rooms[8])
    Board.movePlayerInstance(Board.Players[4], Board.Rooms[10]) 
    Board.movePlayerInstance(Board.Players[5], Board.Rooms[12]) 
    
    #game loop
    while running:
        #delay 50 ms, and redraw window - these need to be the first lines in the game loop - important
        pygame.time.wait(50)
        window.fill((38,50,56))
        
        # Here is where all the logic from the back end will need to be incorporated. This is the main game loop for the client.
        # Players and rooms will need to be updated each turn. This runs continuously so maybe have
        # a way to poll the server only to see if an update needs to be pushed to client or vice versa?
        # need to check if a player should provide data for an accusation, or to disprove
        
        # Draw the board after data has been updated
        # Board.draw calls custom Draw function on each player and room
        Board.draw(window)

            
        #this needs to be the last line in the game loop - important
        pygame.display.flip()


#Stub to mimic the initalize call which will originate from the SERVER
#should pass in player data
initialize("this should be all the game data, specifically to initialize player and turn data")
