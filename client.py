import pygame

from Card import Card
from InputBox import InputBox
from clientNetwork import Network
from Player import Player
from Map import Map
from ClueBoard import ClueBoard
from Button import Button

pygame.init()

width = 800
height = 1000
dimension = 5
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
map = Map().map
font = pygame.font.SysFont("monospace", 30)
output_box = InputBox(50, 900, 700, 48, font)
buttonColor = pygame.Color("grey")
buttonStartX = 25
buttonStartY = 600
buttonW = 150
buttonH = 50
buttons = [Button(buttonColor, buttonStartX, buttonStartY, buttonW, buttonH),
           Button(buttonColor, buttonStartX + 200, buttonStartY, buttonW, buttonH),
           Button(buttonColor, buttonStartX + 400, buttonStartY, buttonW, buttonH),
           Button(buttonColor, buttonStartX + 600, buttonStartY, buttonW, buttonH),
           Button(buttonColor, buttonStartX, buttonStartY + 100, buttonW, buttonH),
           Button(buttonColor, buttonStartX + 200, buttonStartY + 100, buttonW, buttonH),
           Button(buttonColor, buttonStartX + 400, buttonStartY + 100, buttonW, buttonH),
           Button(buttonColor, buttonStartX + 600, buttonStartY + 100, buttonW, buttonH)]
buttonTitles = ['', '', '', '', '', '', '', '']


def redraw_window(board):
    board.draw(win)
    display_text_box()
    display_buttons()
    pygame.display.update()


def display_buttons():
    pygame.draw.rect(win, pygame.Color("black"), pygame.Rect(0, 600, 800, 200))
    for i in range(0, len(buttons)):
        buttons[i].setText(buttonTitles[i])
        buttons[i].draw(win)


def display_text_box():
    pygame.draw.rect(win, pygame.Color("white"), pygame.Rect(0, 700, 800, 300))
    output_box.draw(win)


def execute_player_turn():
    print("execute")


def notify_player_of_win():
    print("notify")


# Sends text input to the server
def check_and_send_card_input(cards, n):
    if isinstance(cards,list):
        for i in cards:
            if not isinstance(i, Card):
                return False
    else:
        if not isinstance(cards, Card):
            return False
    return n.send(cards)


# Updates the board and pulls text input
def update_board(board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    output_box.update()
    redraw_window(board)


def wait_for_button_press(board):
    buttonTitlePressed = ""
    while (buttonTitlePressed == ""):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.isOver(pygame.mouse.get_pos()):
                        buttonTitlePressed = button.text
                        if buttonTitlePressed == "Next...":
                            set_button_titles_rooms_2(board)
                            buttonTitlePressed = ""
                        elif buttonTitlePressed == "Back...":
                            set_button_titles_rooms_1(board)
                            buttonTitlePressed = ""
    return buttonTitlePressed


def get_board_info(n):
    return n.send("get_board")


def check_and_make_board(new_player_info, old_player_info, board):
    if new_player_info != old_player_info:
        return ClueBoard(new_player_info)
    else:
        return board


# Checks the inputted move vs possible moves
def get_player_move(input, p, board):
    moveOptions = board.Players[p].get_possible_moves()

    if input == "North":
        newMove = moveOptions[1][moveOptions[0].index('n')]
        return board.movePlayerInstance(board.Players[p], board.Rooms[newMove])
    elif input == "West":
        newMove = moveOptions[1][moveOptions[0].index('w')]
        return board.movePlayerInstance(board.Players[p], board.Rooms[newMove])
    elif input == "East":
        newMove = moveOptions[1][moveOptions[0].index('e')]
        return board.movePlayerInstance(board.Players[p], board.Rooms[newMove])
    elif input == "South":
        newMove = moveOptions[1][moveOptions[0].index('s')]
        return board.movePlayerInstance(board.Players[p], board.Rooms[newMove])
    elif input == "Tunnel":
        return board.movePlayerInstance(board.Players[p], board.Rooms[10])
    return False

def set_button_titles_disproving(board, newButtonTitles):
    for i in range(0,7):
        if i < len(newButtonTitles):
            buttonTitles[i] = newButtonTitles[i]
        else:
            buttonTitles[i] = ""
    update_board(board)

def set_button_titles_for_move(p, board):
    moveOptions = (board.Players[p].get_possible_moves())[0]
    for i in range(len(buttonTitles)):
        if i < len(moveOptions):
            move = moveOptions[i]
            if move == 'n':
                buttonTitles[i] = "North"
            elif move == 'w':
                buttonTitles[i] = "West"
            elif move == 's':
                buttonTitles[i] = "South"
            elif move == 'e':
                buttonTitles[i] = "East"
            else:
                buttonTitles[i] = "Tunnel"
        else:
            buttonTitles[i] = ''
    update_board(board)


def set_button_titles_weapons(board):
    weapons = ['Rope', 'Knife', 'Pipe', 'Candlestick', 'Revolver', 'Wrench', '', '']
    for i in range(len(buttonTitles)):
        buttonTitles[i] = weapons[i]
    update_board(board)


def set_button_titles_players(board):
    players = ['Scarlet', 'Mustard', 'Green', 'Peacock', 'Plum', 'White', '', '']
    for i in range(len(buttonTitles)):
        buttonTitles[i] = players[i]
    update_board(board)


def set_button_titles_rooms_1(board):
    rooms = ['Study', 'Hall', 'Lounge', 'Library', 'Billiard', 'Dining', 'Conservatory', 'Next...']
    for i in range(len(buttonTitles)):
        buttonTitles[i] = rooms[i]
    update_board(board)


def set_button_titles_rooms_2(board):
    rooms = ['Ball', 'Kitchen', '', '', '', '', '', 'Back...']
    for i in range(len(buttonTitles)):
        buttonTitles[i] = rooms[i]
    update_board(board)


def clear_button_titles(board):
    clearTitles = ['', '', '', '', '', '', '', '']
    for i in range(len(buttonTitles)):
        buttonTitles[i] = clearTitles[i]
    update_board(board)


def get_suggestion(p, board):
    suggestion = [Card(board.Players[p].room.capitalize())]
    set_button_titles_weapons(board)
    suggestion.append(Card(wait_for_button_press(board)))
    set_button_titles_players(board)
    suggestion.append(Card(wait_for_button_press(board)))
    return suggestion

def get_assumption(board):
    suggestion = []
    set_button_titles_weapons(board)
    suggestion.append(Card(wait_for_button_press(board)))
    set_button_titles_players(board)
    suggestion.append(Card(wait_for_button_press(board)))
    set_button_titles_rooms_1(board)
    suggestion.append(Card(wait_for_button_press(board)))
    return suggestion

def main():
    run = True
    n = Network()
    p = n.getP()  # p is the index of the client's player object in the board array
    pygame.display.set_caption("Player " + str(p + 1))
    player_info = get_board_info(n)
    Board = ClueBoard(player_info)
    clock = pygame.time.Clock()
    redraw_window(Board)

    while run:
        clock.tick(60)

        clear_button_titles(Board)


        # Pulls the current game state from server i.e. turn/suggestion/disprove. This needs a better way of displaying then current
        message = n.send("get_state")
        if message != "wait":
            output_box.text = message
        elif output_box.text == "turn":
            output_box.text = ""
        if message == "disprove":
            suggestion = n.send("get_suggestion")
            output_box.text = "disprove " + suggestion[0].name
        elif message == "unable_to_disprove":
            output_box.text = "unable to disprove"
            n.send("change_turn")
        elif message.startswith("disproved"):
            output_box.text = message
            n.send("change_turn")
        elif message == "game_over":
            output_box.text = n.send("get_message")

        # Pulls the current player data from the server, checks for changes and updates the board if needed.
        new_info = get_board_info(n)
        Board = check_and_make_board(new_info, player_info, Board)
        player_info = new_info
        # Updates the board and gets text input. The Board needs to be updated every loop
        update_board(Board)

        if message == "turn":
            set_button_titles_for_move(p, Board)
            buttonInput = wait_for_button_press(Board)
            if get_player_move(buttonInput, p, Board):
                # Checks if in a hallway or not to tell server if it is going to make a suggestion or not. Need a better way to do this
                newMessage = "moved_room"
                if len(Board.Players[p].room) < 4:
                    newMessage = "moved_hall"

                n.send([Board.Players[p].create_player_obj(), newMessage])
        elif message == "suggestion":
            suggestion = get_suggestion(p, Board)
            check_and_send_card_input(suggestion, n)
        elif message == "disprove":
            possibleDisproveCards = []
            # Checks if the user is able to disprove the suggestion, and if they are unable immediately ends their disproving state
            for suggestedCard in suggestion:
                for card in Board.Players[p].hand:
                    if card.name == suggestedCard.name:
                        possibleDisproveCards.append(card.name)
            if len(possibleDisproveCards) == 0:
                n.send("unable_to_disprove")
                output_box.text = "unable to disprove " + suggestion[0].name
            else:
                set_button_titles_disproving(Board, possibleDisproveCards)
                buttonInput = wait_for_button_press(Board)

                check_and_send_card_input(Card(buttonInput), n)
        elif message == "assume":
            assumption = get_assumption(Board)
            check_and_send_card_input(assumption, n)


main()
