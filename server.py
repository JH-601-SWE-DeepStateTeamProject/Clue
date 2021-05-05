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
personalMessagesCards = [[],[],[],[],[],[]]
suggestion = []
answer = []
playerTurn = 0
currentDisprover = 1
outputAllMessage = ""
outputAllMessageCards = []
pygame.init()
Players = []
hands = [[],[],[],[],[],[]]
movedPlayers = [False, False, False, False, False, False] # Keeps track of players moved by suggestion
roomNums = [0,2,4,8,10,12,16,18,20]
playerNames = ['Scarlet', 'Mustard', 'Green', 'Peacock', 'Plum', 'White']


def threaded_client(conn, player):
    global playerTurn
    global currentDisprover
    global outputAllMessage
    global outputAllMessageCards
    global personalMessagesCards
    global answer
    global Board
    conn.send(pickle.dumps(player))
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
            elif data == "get_personal_cards":
                reply = personalMessagesCards[player]
            elif data == "get_suggestion":
                reply = suggestion
            elif data == "get_message":
                reply = outputAllMessage
            elif data == "get_message_cards":
                reply = outputAllMessageCards
            elif data == "change_turn":
                movedPlayers[player] = False
                change_turn(player)
            elif data == "get_player_turn":
                reply = playerTurn
            elif data == "get_answer":
                reply = answer

            elif data == "unable_to_disprove":
                currentDisprover = (currentDisprover + 1) % currentPlayer
                if currentDisprover == playerTurn:
                    messages[playerTurn] = "unable_to_disprove"
                else:
                    messages[currentDisprover] = "disprove"
                messages[player] = "disprove wait"

            elif data == "was_i_moved":
                reply = movedPlayers[player]

            elif isinstance(data, Card):
                if messages[player] == "disprove":
                    outputAllMessage = "The suggestion was disproved."
                    personalMessagesCards[playerTurn] = [data.name]
                    messages[playerTurn] = "disproved"
                    messages[player] = "wait"
                    reply = messages[player]

            elif isinstance(data[0], Card):
                isSuggestion = data.pop(3)

                if isSuggestion:
                    outputAllMessage = "Player " + str(playerTurn + 1) + " is making a suggestion."
                    suggestion.clear()
                    for card in data:
                        # If the card is a player card, move that player to the current players room.
                        if card.name in playerNames:
                            Players[playerNames.index(card.name)].room = Players[player].room
                            movedPlayers[playerNames.index(card.name)] = True
                        suggestion.append(card)
                    outputAllMessageCards = suggestion
                    for i in range(len(messages)):
                        messages[i] = "disprove wait"
                    messages[player] = "suggestion wait"
                    messages[(player + 1) % currentPlayer] = "disprove"
                    print(messages)
                    reply = messages[player]
                    currentDisprover = (player + 1) % currentPlayer
                else:
                    if data[0].name == answer[0].name and data[1].name == answer[1].name and data[2].name == answer[2].name:
                        outputAllMessage = "Player " + str(playerTurn + 1) + " wins! Answer is: "
                        for i in range(len(messages)):
                            messages[i] = "game_over"
                        outputAllMessageCards = answer
                        reply = True
                    else:
                        print(data)
                        change_turn(player)
                        outputAllMessage = "Player " + str(playerTurn + 1) + " loses. Guessed: "
                        outputAllMessageCards.clear()
                        for card in data:
                            outputAllMessageCards.append(card)
                        reply = False

            elif isinstance(data[0], Player):
                Players[player].room = data[0].room
                if data[1] == "moved_room":
                    messages[player] = "suggestion"
                elif data[1] == "moved_hall":
                    messages[player] = "end_turn"
                reply = messages[player]
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()


def change_turn(playerNum):
    global playerTurn
    global outputAllMessage
    outputAllMessageCards.clear()
    outputAllMessage = ""
    for i in range(len(messages)):
        messages[i] = "wait"
    messages[playerNum] = "turn"
    messages.insert(0, messages.pop())
    playerTurn = (playerTurn + 1) % currentPlayer


def setup_game():
    random.shuffle(roomNums)
    for i in range(6):
        Players.append(Player(roomNums[i], i, []))
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
    deck = weapons + people + rooms
    random.shuffle(deck)
    for i in range(len(deck)):
        if currentPlayer != 0:
            hands[i % currentPlayer].append(deck[i])
    for i in range(currentPlayer):
        Players[i].hand = hands[i]
    for i in answer:
        print(i.name)

currentPlayer = 0
setup_game()
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    if currentPlayer != 0:
        messages.append("wait")
    currentPlayer += 1
    assign_cards_to_role()
    start_new_thread(threaded_client, (conn, currentPlayer-1))
