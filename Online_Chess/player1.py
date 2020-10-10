import pygame, threading
from imports.game import Game

startgame = False
pygame.init()
win = pygame.display.set_mode((512, 512))
pygame.display.set_caption('Chess Game')
game = Game(win, 0)

def recv_start_msg(socket):
    global startgame
    while True:
        msg = socket.recv(4).decode()
        if msg == '!':
            print('Game Started')
            startgame = True
            game.t.start()
            break

t = threading.Thread(target=recv_start_msg, args=[game.socket])
t.daemon = True
t.start()
run = True
while run:
    pygame.time.delay(40)
    win.fill((115, 144, 83))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP and startgame:
            mouseX, mouseY = pygame.mouse.get_pos()
            game.click(mouseX, mouseY)

    game.draw_board()
    game.draw_chess()
    game.draw_valid_moves()
    game.check()
    game.draw_game_result()
    pygame.display.update()

pygame.quit()
