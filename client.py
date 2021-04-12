import pygame

from Card import Card
from InputBox import InputBox
from clientNetwork import Network
from Player import Player
from Map import Map
from ClueBoard import ClueBoard

pygame.init()

width = 800
height = 1000
dimension = 5
sq_size = 100
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
map = Map().map
font = pygame.font.SysFont("monospace", 30)
input_box = InputBox(50, 750, 700, 48, font)
output_box = InputBox(50, 900, 700, 48, font)

def redraw_window(player, board):
    board.draw(win)
    display_players_cards(player, board)
    display_text_box()
    pygame.display.update()


def display_players_cards(p, board):
    pygame.draw.rect(win, pygame.Color("white"), pygame.Rect(0, 600, 800, 100))
    x = 10
    y = 650
    cardSize = 50
    hand = board.Players[p].hand
    for card in hand:
        name = card.name
        img = font.render(name, True, pygame.Color("black"))
        win.blit(img, (x, y))
        x += cardSize
        if x >= width:
            x = 10
            y += cardSize


def display_text_box():
    pygame.draw.rect(win, pygame.Color("white"), pygame.Rect(0, 700, 800, 300))
    input_box.draw(win)
    output_box.draw(win)


def execute_player_turn():
    print("execute")


def notify_player_of_win():
    print("notify")


def check_and_send_card_input(textInput, n):
    if isinstance(textInput, str):
        if textInput != "":
            return n.send(Card(textInput))


def update_board(p, board):
    textInput = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        textInput = input_box.handle_event(event)
    input_box.update()
    output_box.update()
    redraw_window(p, board)
    return textInput

def get_board_info(n):
    return n.send("get_board")

def check_and_make_board(new_player_info,old_player_info, board):
    if new_player_info != old_player_info:
        return ClueBoard(new_player_info)
    else:
        return board

def get_player_move(input, p, board):
    moveOptions = board.Players[p].get_possible_moves()
    if input == "n" and input in moveOptions[0]:
        newMove = moveOptions[1][moveOptions[0].index(input)]
        return board.movePlayerInstance(board.Players[p],board.Rooms[newMove])
    elif input == "w" and input in moveOptions[0]:
        newMove = moveOptions[1][moveOptions[0].index(input)]
        return board.movePlayerInstance(board.Players[p],board.Rooms[newMove])
    elif input == "e" and input in moveOptions[0]:
        newMove = moveOptions[1][moveOptions[0].index(input)]
        return board.movePlayerInstance(board.Players[p],board.Rooms[newMove])
    elif input == "s" and input in moveOptions[0]:
        newMove = moveOptions[1][moveOptions[0].index(input)]
        return board.movePlayerInstance(board.Players[p],board.Rooms[newMove])


def main():
    run = True
    n = Network()
    p = n.getP()
    player_info = get_board_info(n)
    Board = ClueBoard(player_info)
    clock = pygame.time.Clock()
    redraw_window(p, Board)

    while run:
        clock.tick(60)
        new_info = get_board_info(n)
        Board = check_and_make_board(new_info,player_info, Board)
        player_info = new_info
        message = n.send("get_state")
        output_box.text = message  # need a better way to display the game state.
        if message == "disprove":
            suggestion = n.send("get_suggestion")
            output_box.text = "disprove " + suggestion[0].name
        elif message == "unable_to_disprove":
            output_box.text = "unable to disprove"
            n.send("change_turn")
        elif message == "disproved":
            suggestion = n.send("get_suggestion")
            output_box.text = "disproved " + suggestion[0].name
            n.send("change_turn")
        elif message == "game_over":
            output_box.text = n.send("get_message")
        textInput = update_board(p, Board)
        if message == "turn":
            if get_player_move(textInput, p, Board):
                # Checks if in a hallway or not to tell server if it is going to make a suggestion or not. Need a better way to do this
                newMessage = "moved_room"
                if len(Board.Players[p].room) < 4:
                    newMessage = "moved_hall"

                n.send([Board.Players[p].create_player_obj(),newMessage])
        elif message == "suggestion":
            check_and_send_card_input(textInput, n)
        elif message == "disprove":
            flag = False
            for card in Board.Players[p].hand:
                if card.name == suggestion[0].name:
                    flag = True
            if not flag:
                n.send("unable_to_disprove")
                output_box.text = "unable to disprove " + suggestion[0].name
            else:
                check_and_send_card_input(textInput, n)
        elif message == "assume":
            check_and_send_card_input(textInput, n)


main()
