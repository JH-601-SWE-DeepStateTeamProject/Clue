import socket
from _thread import *
from Card import Card
from Deck import Deck
from ClueBoard import ClueBoard
from Player import Player
import pygame
import pickle
import random

server = socket.gethostname()
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

messages = ["turn"]
suggestion = []
answer = []
playerTurn = 0
currentDisprover = 1
outputAllMessage = ""
pygame.init()
Players = []
hands = [[],[],[],[],[],[]]
roomNums = [0,2,4,8,10,12,16,18,20]
playerNames = ['Scarlet', 'Mustard', 'Green', 'Peacock', 'Plum', 'White']


def threaded_client(conn, player):
    global playerTurn
    global currentDisprover
    global outputAllMessage
    global answer
    global Board
    conn.send(pickle.dumps(player))
    turnCount = 0
    #Should have a seperate while loop here to hold players in a pregame state in order to properly randomize cards/starting positions

    #The actual game runs in this while loop
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            reply = ""

            if not data:
                print("Disconnected")
                break
            elif data == "get_board":
                reply = Players
            elif data == "get_state":
                reply = messages[player]
            elif data == "get_suggestion":
                reply = suggestion
            elif data == "get_message":
                reply = outputAllMessage

            elif data == "change_turn":
                # Used to force assuming currently.
                if turnCount == 3:
                    messages[player] = "assume"
                else:
                    turnCount += 1
                    change_turn(player)

            elif data == "unable_to_disprove":
                currentDisprover = (currentDisprover + 1) % len(Players)
                if currentDisprover == playerTurn:
                    messages[playerTurn] = "unable_to_disprove"
                    messages[player] = "wait"
                else:
                    messages[currentDisprover] = "disprove"

            elif isinstance(data, Card):
                if messages[player] == "disprove":
                    messages[playerTurn] = "disproved with " + data.name
                    messages[player] = "wait"
                    reply = messages[player]

            elif isinstance(data[0], Card):
                if messages[player] == "suggestion":
                    suggestion.clear()
                    for card in data:

                        # If the card is a player card and the player exists, move that player to the current players room.
                        if card.name in playerNames:
                            if playerNames.index(card.name) < len(Players):
                                Players[playerNames.index(card.name)].room = Players[player].room
                        suggestion.append(card)
                    messages[player] = "suggestion wait"
                    messages[(player + 1) % len(Players)] = "disprove"
                    reply = messages[player]
                    currentDisprover = (player + 1) % len(Players)
                elif messages[player] == "assume":
                    if data[0].name == answer[0].name and data[1].name == answer[1].name and data[2].name == answer[2].name:
                        outputAllMessage = "Player " + str(playerTurn + 1) + " wins! Answer: " + answer.name
                        for i in range(len(messages)):
                            messages[i] = "game_over"
                        reply = [outputAllMessage] + Players
                    else:
                        outputAllMessage = "Player " + str(playerTurn + 1) + " loses. Guessed " + data.name
                        messages[player] = "guessed_wrong"
                        reply = [outputAllMessage] + Players
            elif isinstance(data[0], Player):
                Players[player].room = data[0].room
                if data[1] == "moved_room":
                    messages[player] = "suggestion"
                elif data[1] == "moved_hall":
                    turnCount += 1
                    change_turn(player)
                reply = messages[player]
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()


def change_turn(playerNum):
    global playerTurn
    messages[playerNum] = "turn"
    messages.insert(0, messages.pop())
    playerTurn = (playerTurn + 1) % len(Players)


def connect_players():
    print("connect")


def assign_player_roles():
    print("assign")

def setup_game():
    random.shuffle(roomNums)
    assign_cards_to_role()

#Should be run when game is started, randomizes deck, creates the answer and deals the cards
def assign_cards_to_role():
    deck_obj = Deck()
    weapons = deck_obj.weapons  # + deck_obj.people + deck_obj.rooms
    people = deck_obj.people
    rooms = deck_obj.rooms
    random.shuffle(weapons)
    random.shuffle(people)
    random.shuffle(rooms)
    answer.clear()
    answer.append(weapons.pop())
    answer.append(people.pop())
    answer.append(rooms.pop())
    for i in hands:
        i.clear()
    deck = weapons #+ people + rooms
    random.shuffle(deck)
    for i in range(len(deck)):
        hands[i % (currentPlayer + 1)].append(deck[i])
    for i in range(len(Players)):
        Players[i].hand = hands[i]



def store_game_state():
    print("store")


def store_player_locations():
    print("store_player")


def player_guess_monitoring():
    print("monitor")


def organize_player_turns():
    print("organize")


def determine_game_winner():
    print("determine")


currentPlayer = 0
setup_game()
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    assign_cards_to_role()
    Players.append(Player(roomNums[currentPlayer],currentPlayer,hands[currentPlayer]))
    if currentPlayer != 0:
        messages.append("wait")

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
