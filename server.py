import socket
from _thread import *
from Player import Player
import pickle

server = "192.168.1.98" #just using local IP address right now - need to replace with permanent IP of server at some point
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


players = [Player(0,0,50,50,(255,0,0)), Player(100,100, 50,50, (0,0,255))]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

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