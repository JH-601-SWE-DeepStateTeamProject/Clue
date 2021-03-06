import os
import pygame

from Card import Card
from clientNetwork import Network
from Player import Player
from Map import Map
from ClueBoard import ClueBoard
from Button import Button, MenuButton

pygame.init()

width = 800
height = 900
dimension = 5
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
map = Map().map
font = pygame.font.SysFont("monospace", 20)
buttonColor = pygame.Color("grey")
buttonStartX = 25
buttonStartY = 720
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

menu_btns = [MenuButton("Three Players", 355, 200, (135,206,250)),
        MenuButton("Four Players", 355, 275, (135,206,250)),
        MenuButton("Five Players", 355, 350, (135,206,250)),
        MenuButton("Six Players", 355, 425, (135,206,250))]

def redraw_window(board):
    board.draw(win)
    display_buttons()
    pygame.display.update()


def display_outputall_message(message, cards=[]):
    surf = pygame.Surface((800, 60))
    surf.fill((0, 0, 0))
    rect = surf.get_rect()
    rect.x = 0
    rect.y = 600
    label = font.render(message, 1, (255, 255, 255))
    win.blit(surf, rect)
    win.blit(label, [rect.x + (rect.width / 2) - ((label.get_width() + (len(cards) * 80)) / 2),
                     rect.y + (rect.height / 2) - (label.get_height() / 2)])


    for idx, card in enumerate(cards):
        if isinstance(card,Card):
            loadNameStr = (card.name).lower()
            if os.path.exists("images/card_" + loadNameStr + ".png"):
                cardImg = pygame.image.load(os.path.abspath("images/card_" + loadNameStr + ".png"))
                cardImg = pygame.transform.scale(cardImg, (70, 40))
                yVal = rect.y + 5
                xVal = (rect.x + (rect.width / 2) + ((label.get_width() + (len(cards) * 80)) / 2)) - (
                        len(cards) * 80) + (idx * 80)
                win.blit(cardImg, (xVal, yVal))
        else:
            loadNameStr = card.lower()
            if os.path.exists("images/card_" + loadNameStr + ".png"):
                cardImg = pygame.image.load(os.path.abspath("images/card_" + loadNameStr + ".png"))
                cardImg = pygame.transform.scale(cardImg, (70, 40))
                yVal = rect.y + 5
                xVal = (rect.x + (rect.width / 2) + ((label.get_width() + (len(cards) * 80)) / 2)) - (len(cards) * 80) + (
                            idx * 80)
                win.blit(cardImg, (xVal, yVal))


def display_personal_message(message, cards=[]):
    surf = pygame.Surface((800, 60))
    surf.fill((0, 0, 0))
    rect = surf.get_rect()
    rect.x = 0
    rect.y = 660
    label = font.render(message, 1, (255, 255, 255))
    win.blit(surf, rect)
    win.blit(label, [rect.x + (rect.width / 2) - ((label.get_width() + (len(cards) * 80)) / 2),
                     rect.y + (rect.height / 2) - (label.get_height() / 2)])
    for idx, card in enumerate(cards):
        if isinstance(card, Card):
            loadNameStr = (card.name).lower()
            if os.path.exists("images/card_" + loadNameStr + ".png"):
                cardImg = pygame.image.load(os.path.abspath("images/card_" + loadNameStr + ".png"))
                cardImg = pygame.transform.scale(cardImg, (70, 40))
                yVal = rect.y + 5
                xVal = (rect.x + (rect.width / 2) + ((label.get_width() + (len(cards) * 80)) / 2)) - (
                        len(cards) * 80) + (idx * 80)
                win.blit(cardImg, (xVal, yVal))
        else:
            loadNameStr = card.lower()
            if os.path.exists("images/card_" + loadNameStr + ".png"):
                cardImg = pygame.image.load(os.path.abspath("images/card_" + loadNameStr + ".png"))
                cardImg = pygame.transform.scale(cardImg, (70, 40))
                yVal = rect.y + 5
                xVal = (rect.x + (rect.width / 2) + ((label.get_width() + (len(cards) * 80)) / 2)) - (
                            len(cards) * 80) + (
                               idx * 80)
                win.blit(cardImg, (xVal, yVal))


def display_buttons():
    pygame.draw.rect(win, pygame.Color("black"), pygame.Rect(0, buttonStartY, 800, 200))
    for i in range(0, len(buttons)):
        buttons[i].setText(buttonTitles[i])
        buttons[i].draw(win)


# Sends text input to the server
def check_and_send_card_input(cards, n, isSuggestion):
    if isinstance(cards, list):
        for i in cards:
            if not isinstance(i, Card):
                return False
        cards.append(isSuggestion)
    else:
        if not isinstance(cards, Card):
            return False
    return n.send(cards)


# Updates the board and pulls text input
def update_board(board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
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


def check_and_make_board(new_player_info, old_player_info, board, p, player_turn):
    if new_player_info != old_player_info:
        return ClueBoard(new_player_info, p, player_turn)
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
    for i in range(0, 7):
        if i < len(newButtonTitles):
            buttonTitles[i] = newButtonTitles[i]
        else:
            buttonTitles[i] = ""
    update_board(board)


def set_button_titles_for_move(p, board, firstTurn):
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
                if firstTurn:
                    buttonTitles[i] = ''
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


def set_button_titles_turn_choice(board, move, suggestion, end_turn):
    titles = []
    if move:
        titles.append("Move")
    if suggestion:
        titles.append("Make Suggestion")
    if end_turn:
        titles.append("End Turn")
    for i in range(len(buttonTitles)):
        if i < len(titles):
            buttonTitles[i] = titles[i]
        elif i == 7:
            buttonTitles[i] = "Make Assumption"
        else:
            buttonTitles[i] = ""

    update_board(board)


def clear_button_titles(board):
    clearTitles = ['', '', '', '', '', '', '', '']
    for i in range(len(buttonTitles)):
        buttonTitles[i] = clearTitles[i]
    update_board(board)


def get_suggestion(p, board):
    suggestion = []
    set_button_titles_weapons(board)
    suggestion.append(Card(wait_for_button_press(board)))
    set_button_titles_players(board)
    suggestion.append(Card(wait_for_button_press(board)))
    suggestion.append(Card(board.Players[p].room.capitalize()))
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


def fullScreen():
    while True:
        win.fill((0,0,0))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Lobby is full", 1, (255, 255, 255), True)
        win.blit(text, (width/2 - text.get_width()/2, height/8 - text.get_height()/2))

        pygame.display.update()

def getLimit(n):
    player_limit = n.send("player_limit")
    return player_limit


def getAmountOfPlayers(n):
    amount_players = n.send("get_amount_players")
    return amount_players


def waitingScreen(p, n):
    win.fill((0,0,0))

    if p == 0:
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("How Many Players?...", 1, (255, 255, 255), True)
        win.blit(text, (width/2 - text.get_width()/2, height/8 - text.get_height()/2))

        for btn in menu_btns:
            btn.draw(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in menu_btns:
                    if btn.click(pos):
                        n.send(btn.text)
                        print(btn.text)

    else:
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Game not available, please wait...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    pygame.display.update()


def waiting_for_players():
    win.fill((0,0,0))
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render("Waiting for players to join, please wait...", 1, (255, 0, 0), True)
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()


def main():
    firstTurn = True
    run = True
    lost = False
    n = Network()
    p = n.getP()  # p is the index of the client's player object in the board array
    clock = pygame.time.Clock()

    while getLimit(n) < 3:
        clock.tick(60)
        waitingScreen(p, n)

    while getLimit(n) > getAmountOfPlayers(n):
        clock.tick(60)
        waiting_for_players()

    if p > getLimit(n) - 1:
        clock.tick(60)
        fullScreen()
    win.fill((0, 0, 0))

    pygame.display.set_caption("Player " + str(p + 1))
    player_info = get_board_info(n)
    player_turn = n.send("get_player_turn")
    Board = ClueBoard(player_info, p, player_turn)
    clock = pygame.time.Clock()
    redraw_window(Board)


    while run:
        clock.tick(60)

        clear_button_titles(Board)

        player_turn = n.send("get_player_turn")
        display_outputall_message(n.send("get_message"), n.send("get_message_cards"))

        # Pulls the current game state from server i.e. turn/suggestion/disprove. This needs a better way of displaying then current
        message = n.send("get_state")
        if message == "disprove":
            suggestion = n.send("get_suggestion")
            display_personal_message("Your turn to disprove.")
        elif message == "unable_to_disprove":
            suggestion = n.send("get_suggestion")
            display_personal_message("Your suggestion was unable to be disproved. ", suggestion)
        elif message == "disproved":
            display_personal_message("Your suggestion was disproved with ", n.send("get_personal_cards"))
        elif message == "disprove wait":
            display_personal_message("")

        # Pulls the current player data from the server, checks for changes and updates the board if needed.
        new_info = get_board_info(n)
        Board = check_and_make_board(new_info, player_info, Board, p, player_turn)
        player_info = new_info
        # Updates the board and gets text input. The Board needs to be updated every loop
        update_board(Board)

        if message == "turn" or message == "suggestion" or message == "end_turn":
            if lost:
                n.send("change_turn")
                continue
            if message == "turn":
                canSuggest = n.send("was_i_moved")
                canMove = Board.canIMove(p, firstTurn)
                if canMove:
                    canEnd = False
                else:
                    display_personal_message("Unable to move. All possible moves are blocked.")
                    canEnd = True
                set_button_titles_turn_choice(Board, canMove, canSuggest, canEnd)
            elif message == "suggestion":
                display_personal_message("")
                set_button_titles_turn_choice(Board, False, True, True)
            elif message == "end_turn":
                set_button_titles_turn_choice(Board, False, False, True)
            buttonInput = wait_for_button_press(Board)
            display_personal_message("")
            if buttonInput == "Move":
                set_button_titles_for_move(p, Board, firstTurn)
                firstTurn = False
                buttonInput = wait_for_button_press(Board)
                if get_player_move(buttonInput, p, Board):
                    display_personal_message("")
                    # Checks if in a hallway or not to tell server if it is going to make a suggestion or not.
                    if len(Board.Players[p].room) < 4:
                        newMessage = "moved_hall"
                    else:
                        newMessage = "moved_room"
                    n.send([Board.Players[p].create_player_obj(), newMessage])
                else:
                    display_personal_message("This hallway is blocked. Please select a different move.")
            elif buttonInput == "Make Suggestion":
                suggestion = get_suggestion(p, Board)
                check_and_send_card_input(suggestion, n, True)
            elif buttonInput == "Make Assumption":
                assumption = get_assumption(Board)
                answer = check_and_send_card_input(assumption, n, False)
                if answer:
                    display_personal_message("You win, answer is: ", n.send("get_answer"))
                    # Winning stuff here
                else:
                    lost = True
                    display_personal_message("You lost, answer is: ", n.send("get_answer"))
            elif buttonInput == "End Turn":
                n.send("change_turn")
        elif message == "disprove":
            possibleDisproveCards = []
            # Checks if the user is able to disprove the suggestion, and if they are unable immediately ends their disproving state
            for suggestedCard in suggestion:
                for card in Board.Players[p].hand:
                    if card.name == suggestedCard.name:
                        possibleDisproveCards.append(card.name)
            if len(possibleDisproveCards) == 0:
                n.send("unable_to_disprove")
                display_personal_message("")
            else:
                set_button_titles_disproving(Board, possibleDisproveCards)
                buttonInput = wait_for_button_press(Board)
                display_personal_message("")
                check_and_send_card_input(Card(buttonInput), n, False)
        elif message == "unable_to_disprove" or message == "disproved":
            set_button_titles_turn_choice(Board, False, False, True)
            buttonInput = wait_for_button_press(Board)
            if buttonInput == "Make Assumption":
                assumption = get_assumption(Board)
                answer = check_and_send_card_input(assumption, n, False)
                if answer:
                    display_personal_message("You win, answer is: ", n.send("get_answer"))
                    # Winning stuff here
                else:
                    lost = True
                    display_personal_message("You lost, answer is: ", n.send("get_answer"))
            elif buttonInput == "End Turn":
                n.send("change_turn")


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Click to start!", 1, (255, 255, 255), True)
        win.blit(text, (width/2 - text.get_width()/2, height/8 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()
