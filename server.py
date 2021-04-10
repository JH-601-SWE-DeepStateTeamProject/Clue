import socket
from _thread import *

from Card import Card
from Player import Player
import pickle

server = socket.gethostname()
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

answer = Card("11")

s.listen()
print("Waiting for a connection, Server Started")

players = [Player(0, 0, 50, 50, (255, 0, 0), ["1", "2", "3", "4", "5"]), Player(450, 450, 50, 50, (0, 0, 255), ["6", "7", "8", "9", "10"])]
messages = ["turn", "wait"]
suggestion = []
playerTurn = 0
currentDisprover = 1
outputAllMessage = ""


def threaded_client(conn, player):
    global playerTurn
    global currentDisprover
    global outputAllMessage
    global answer
    conn.send(pickle.dumps(players[player]))
    turnCount = 0
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            reply = ""

            if not data:
                print("Disconnected")
                break

            elif isinstance(data, Player):
                players[player] = data
                reply = players
            elif data == "start":
                reply = players
            elif data == "get_state":
                reply = messages[player]
            elif data == "get_suggestion":
                reply = suggestion
            elif data == "get_message":
                reply = outputAllMessage
            elif data == "moved_room":
                messages[player] = "suggestion"
            elif data == "moved_hall":
                turnCount += 1
                change_turn(player)
            elif data == "change_turn":
                # Used to force assuming currently.
                if turnCount == 3:
                    messages[player] = "assume"
                else:
                    turnCount += 1
                    change_turn(player)

            elif data == "unable_to_disprove":
                currentDisprover = (currentDisprover + 1) % len(players)
                if currentDisprover == playerTurn:
                    messages[playerTurn] = "unable_to_disprove"
                    messages[player] = "wait"

            elif isinstance(data, Card):
                if messages[player] == "suggestion":
                    suggestion.clear()
                    suggestion.append(data)
                    messages[player] = "suggestion wait"
                    messages[(player + 1) % len(players)] = "disprove"
                    reply = messages[player]
                    currentDisprover = (player + 1) % len(players)

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
                        reply = [outputAllMessage] + players
                    else:
                        outputAllMessage = "Player " + str(playerTurn + 1) + " loses. Guessed " + data.name
                        messages[player] = "guessed_wrong"
                        reply = [outputAllMessage] + players

            elif isinstance(data, Player):
                players[player] = data
                if (messages[player]) == "disprove":
                    reply = [messages[player]] + suggestion + players
                elif(messages[player]) == "disproved":
                    reply = [messages[player]] + suggestion + players
                else:
                    reply = [messages[player]] + players

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()


def change_turn(playerNum):
    global playerTurn
    messages[playerNum] = "turn"
    messages.insert(0, messages.pop())
    reply = [messages[playerNum]] + players
    playerTurn = (playerTurn + 1) % len(players)
    return reply


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

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
