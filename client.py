import pygame

from Card import Card
from InputBox import InputBox
from clientNetwork import Network
from Player import Player
from Map import Map

pygame.init()

width = 500
height = 900
dimension = 5
sq_size = 100
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
map = Map().map
font = pygame.font.SysFont(pygame.font.get_default_font(), 48)
input_box = InputBox(50, 650, 200, 48, font)
output_box = InputBox(50, 800, 200, 48, font)


def redraw_window(player, players=[]):
    draw_game_board()
    display_players_cards(player)
    for p in players:
        if isinstance(p, Player):
            p.draw(win)
    display_text_box()
    pygame.display.update()


def get_player_move():
    print("obtain")


def display_players_cards(p):
    pygame.draw.rect(win, pygame.Color("white"), pygame.Rect(0, 500, 500, 100))
    x = 10
    y = 550
    cardSize = 50
    hand = p.hand
    for card in hand:
        name = card.name
        img = font.render(name, True, pygame.Color("black"))
        win.blit(img, (x, y))
        x += cardSize
        if x >= width:
            x = 10
            y += cardSize


def display_text_box():
    pygame.draw.rect(win, pygame.Color("white"), pygame.Rect(0, 600, 500, 300))
    input_box.draw(win)
    output_box.draw(win)


def execute_player_turn():
    print("execute")


def draw_game_board():
    colors = [pygame.Color("white"), pygame.Color("gray"), pygame.Color("black")]

    for r in range(dimension):
        for c in range(dimension):
            square = map[r][c]
            if square == "r":
                color = colors[0]
            elif square == "h":
                color = colors[1]
            else:
                color = colors[2]
            pygame.draw.rect(win, color, pygame.Rect(c * sq_size, r * sq_size, sq_size, sq_size))


def notify_player_of_win():
    print("notify")


def check_and_send_input(textInput, n):
    if isinstance(textInput, str):
        if textInput != "":
            return n.send(Card(textInput))


def update_board(p, players):
    textInput = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        textInput = input_box.handle_event(event)
    input_box.update()
    output_box.update()
    redraw_window(p, players)
    return textInput


def main():
    run = True
    n = Network()
    p = n.getP()
    players = n.send("start")
    clock = pygame.time.Clock()
    redraw_window(p, players)

    while run:
        clock.tick(60)
        players = n.send(p)
        message = n.send("get_state")
        pygame.display.set_caption(message)  # need a better way to display the game state.
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
        textInput = update_board(p, players)
        if message == "turn":
            moved = p.move()
            if moved:
                if p.get_room() == "h":
                    n.send("moved_hall")
                else:
                    n.send("moved_room")
        elif message == "suggestion":
            check_and_send_input(textInput, n)
        elif message == "disprove":
            flag = False
            for card in p.hand:
                if card.name == suggestion[0].name:
                    flag = True
            if not flag:
                n.send("unable_to_disprove")
                output_box.text = "unable to disprove " + suggestion[0].name
            else:
                check_and_send_input(textInput, n)
        elif message == "assume":
            check_and_send_input(textInput, n)


main()
