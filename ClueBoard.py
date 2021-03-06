import pygame
import os
from RoomSprite import RoomSprite
from PlayerSprite import PlayerSprite
from Player import Player
from Card import Card


class ClueBoard:
    # clueboard contains all players, room, and cards
    Players = []
    Rooms = []
    Cards = []  # not yet implemented
    player_turn = 0

    def __init__(self, PlayerData, pNum, player_turn):
        # initialize rooms. hardcoded because the rooms do not change
        # tunnels also handled as room objects for now - this implementation may need to be changed in future
        self.Rooms.extend(
            [RoomSprite("STUDY"), RoomSprite("H1"), RoomSprite("HALL"), RoomSprite("H2"), RoomSprite("LOUNGE"),
             RoomSprite("H3"), RoomSprite("H4"), RoomSprite("H5"),
             RoomSprite("LIBRARY"), RoomSprite("H6"), RoomSprite("BILLIARD"), RoomSprite("H7"), RoomSprite("DINING"),
             RoomSprite("H8"), RoomSprite("H9"), RoomSprite("H10"),
             RoomSprite("CONSERVATORY"), RoomSprite("H11"), RoomSprite("BALL"), RoomSprite("H12"),
             RoomSprite("KITCHEN"),
             RoomSprite("TUNNEL1"), RoomSprite("TUNNEL2"), RoomSprite("TUNNEL3"), RoomSprite("TUNNEL4")
             ])
        # initialize player data. need to use initialization data from server to set up
        # hard-coded for now. need to tie specific players to their unique client id as provided by server. unique id is 3rd parameter
        p1 = PlayerSprite("SCARLET", "INITIAL", 1, [])
        self.Players.append(p1)
        p2 = PlayerSprite("MUSTARD", "INITIAL", 2, [])
        self.Players.append(p2)
        p3 = PlayerSprite("GREEN", "INITIAL", 3, [])
        self.Players.append(p3)
        p4 = PlayerSprite("PEACOCK", "INITIAL", 4, [])
        self.Players.append(p4)
        p5 = PlayerSprite("PLUM", "INITIAL", 5, [])
        self.Players.append(p5)
        p6 = PlayerSprite("WHITE", "INITIAL", 6, [])
        self.Players.append(p6)
        self.player_turn = player_turn
        self.set_data(PlayerData, pNum)

    def set_data(self, PlayerData, pNum):
        for num in range(len(PlayerData)):
            # Change room based on given data
            player_obj = PlayerData[num]
            self.movePlayerInstance(self.Players[num], self.Rooms[player_obj.room])

            # Set cards based on given data
            self.Players[num].hand = player_obj.hand
            if num == pNum:
                self.Cards = player_obj.hand

    # pass in room and player to update
    def movePlayerInstance(self, characterObj, newRoomObj):
        # checks if player is already in the room. this kind of move shouldn't be allowed by back end logic
        if (characterObj.room == newRoomObj.name):
            pass
        else:
            # remove player from old room, append to new room, and update the current room for the player. pass in objects for the player and each room
            # move player sprite to correct room
            if characterObj.room == "INITIAL":
                characterObj.room = ""
            else:
                # checks if new room is a hallway and has a current player. Returns False if so
                if newRoomObj.roomType == "H_HALL" or newRoomObj.roomType == "V_HALL":
                    if len(newRoomObj.playersInRoom) > 0:
                        return False

                # remove the player from their old room
                # iterate through rooms
                for room in self.Rooms:
                    if characterObj.room == room.name:
                        # match on room name. iterate through the player list that the room has
                        for pl in room.playersInRoom:
                            # match on player name
                            if (pl.name == characterObj.name):
                                room.playersInRoom.remove(pl)

            # update the players rect, update their current room. add the player object to that rooms player list
            newPos = newRoomObj.openPlacement()
            characterObj.rect.x = newPos[0]
            characterObj.rect.y = newPos[1]
            characterObj.room = newRoomObj.name
            newRoomObj.playersInRoom.append(characterObj)
            return True

    def draw(self, window):
        for room in self.Rooms:
            room.draw(window)
        for player in self.Players:
            player.draw(window)
        #draw ui to show where cards are placed
        cardBackground = pygame.image.load('images/cardUI.png')
        window.blit(cardBackground, (690,40))
        for idx, card in enumerate(self.Cards):
            if idx < 9:
                #the image loads from the name of the card. all cards are in the format: images/card_%NAMEOFCARD%.png ..... eg: card_billiard.png, card_knife.png, card_mustard.png
                #so the var loadNameStr just needs to contain the name of the character, weapon, or room: eg) billiard, knife, mustard. it is automatically sent to lowercase to match file name
                loadNameStr = (card.name).lower()
                if os.path.exists("images/card_" + loadNameStr + ".png"):
                    cardImg = pygame.image.load(os.path.abspath("images/card_" + loadNameStr + ".png"))
                    cardImg = pygame.transform.scale(cardImg, (70,40))
                    yVal = 82 + (idx * 53)
                    window.blit(cardImg, (695,yVal))

        for i in range(6):
            if i == self.player_turn:
                pygame.draw.rect(window, pygame.Color("green"), pygame.Rect(48, 86 + (i * 36), 2, 30))
            else:
                pygame.draw.rect(window, pygame.Color("black"), pygame.Rect(48, 86 + (i * 36), 2, 30))

    def canIMove(self, p, firstMove):
        room = self.Players[p].room
        hallsToCheck = []
        # Hardcoding this because it can only happen in set scenarios
        if room == "HALL":
            hallsToCheck = [self.Rooms[1], self.Rooms[3], self.Rooms[6]]
        elif room == "LIBRARY":
            hallsToCheck = [self.Rooms[5], self.Rooms[9], self.Rooms[13]]
        elif room == "BILLIARD":
            hallsToCheck = [self.Rooms[6], self.Rooms[9], self.Rooms[11], self.Rooms[14]]
        elif room == "DINING":
            hallsToCheck = [self.Rooms[7], self.Rooms[11], self.Rooms[15]]
        elif room == "BALL":
            hallsToCheck = [self.Rooms[14], self.Rooms[17], self.Rooms[19]]
        elif firstMove:
            if room == "STUDY":
                hallsToCheck = [self.Rooms[1], self.Rooms[5]]
            elif room == "LOUNGE":
                hallsToCheck = [self.Rooms[3], self.Rooms[7]]
            elif room == "CONSERVATORY":
                hallsToCheck = [self.Rooms[13], self.Rooms[17]]
            elif room == "KITCHEN":
                hallsToCheck = [self.Rooms[15], self.Rooms[19]]
        else:
            return True
        for room in hallsToCheck:
            if len(room.playersInRoom) == 0:
                return True
        return False
