import socket
from _thread import *

from Card import Card
from ClueBoard import ClueBoard
from Player import Player
import pygame
import pickle

server = socket.gethostname()
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# Hardcoding hands/answer for now
answer = Card("11")
hands = [[Card("1"),Card("2"),Card("3"),Card("4"),Card("5")],[Card("6"),Card("7"),Card("8"),Card("9"),Card("10")],[],[],[],[]]

s.listen()
print("Waiting for a connection, Server Started")

messages = ["turn"]
suggestion = []
playerTurn = 0
currentDisprover = 1
outputAllMessage = ""
pygame.init()
Players = []


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

            elif isinstance(data, Card):
                if messages[player] == "suggestion":
                    suggestion.clear()
                    suggestion.append(data)
                    messages[player] = "suggestion wait"
                    messages[(player + 1) % len(Players)] = "disprove"
                    reply = messages[player]
                    currentDisprover = (player + 1) % len(Players)

                elif messages[player] == "disprove":
                    if data.name == suggestion[0].name:
                        messages[playerTurn] = "disproved"
                        messages[player] = "wait"
                    reply = messages[player]

                elif messages[player] == "assume":
                    if data.name == answer.name:
                        outputAllMessage = "Player " + str(playerTurn + 1) + " wins! Answer: " + answer.name
                        for i in range(len(messages)):
                            messages[i] = "game_over"
                        reply = [outputAllMessage] + Players
                    else:
                        outputAllMessage = "Player " + str(playerTurn + 1) + " loses. Guessed " + data.name
                        messages[player] = "guessed_wrong"
                        reply = [outputAllMessage] + Players
            elif isinstance(data[0], Player):
                Players[player] = data[0]
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


def assign_cards_to_role():
    print("assign_role")


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
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    Players.append(Player(currentPlayer*2,currentPlayer,hands[currentPlayer]))
    if currentPlayer != 0:
        messages.append("wait")

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
