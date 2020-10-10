import pygame, socket, threading
from .piece import Piece
from .ip import server_ip, server_port

class Game():
    def __init__(self, win, player):
        self.socket = socket.socket()
        self.server_ip = server_ip
        self.server_port = server_port
        print(f'Trying to connect to server at {self.server_ip}')
        self.socket.connect((self.server_ip, self.server_port))
        print('Connected')
        self.t = threading.Thread(target=self.recv_move)
        self.t.daemon = True

        self.win = win
        self.player = player
        self.socket.send(str(self.player).encode())
        self.turn = 0
        self.valid_moves = []
        self.selected_piece = None
        self.pieces = []
        self.board = [
            [2, 3, 4, 5, 6, 4, 3, 2],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-2, -3, -4, -5, -6, -4, -3, -2],
        ]
        self.font = pygame.font.SysFont('comicsansms', 40)
        self.game_result = ''
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    p = Piece(self.board[i][j], self.win, j, i)
                    self.pieces.append(p)

    
    def draw_board(self):
        for i in range(8):
            for j in range(i%2, 8, 2):
                pygame.draw.rect(self.win, (255, 255, 255), (i*64, j*64, 64, 64), 0)
    
    def draw_chess(self):
        for piece in self.pieces:
            piece.show()
    
    def click(self, mouseX, mouseY):
        if self.player == self.turn:
            x = mouseX // 64
            y = mouseY // 64
            if [x, y] in self.valid_moves:
                self.send_move(self.selected_piece, [x, y])
                self.move_piece(self.selected_piece, [x, y])
                self.selected_piece = None
            else:
                for piece in self.pieces:
                    if piece.x == x and piece.y == y and piece.player == self.turn:
                        self.selected_piece = piece
                        self.valid_moves = self.selected_piece.get_valid_moves(self.board)
    
    def move_piece(self, piece, new_pos):
        type = self.board[piece.y][piece.x]
        self.board[piece.y][piece.x] = 0
        if self.turn == self.player:
            print(f'You moved {piece.ptype[piece.type]} from ({piece.x}, {piece.y}) to ({new_pos[0]}, {new_pos[1]})')
        else:
            player = 'White' if self.player == 1 else 'Black' 
            print(f'{player} moved {piece.ptype[piece.type]} from ({piece.x}, {piece.y}) to ({new_pos[0]}, {new_pos[1]})')
        piece.x = new_pos[0]
        piece.y = new_pos[1]
        for Piece in self.pieces:
            if Piece.x == piece.x and Piece.y == piece.y and Piece != piece:
                self.pieces.remove(Piece)
                del Piece
        self.board[piece.y][piece.x] = type
        self.turn = 1 if self.turn == 0 else 0
        piece.first_time = False
        self.valid_moves = []
        
    
    def draw_valid_moves(self):
        for move in self.valid_moves:
            pygame.draw.circle(self.win, (0, 0, 255), (move[0]*64+32, move[1]*64+32), 10)
    
    def check(self):
        for piece in self.pieces:
            if piece.player == 0 and piece.type == 1 and piece.y == 0:
                x = piece.x
                y = piece.y
                piece.__init__(-5, self.win, x, y)
            elif piece.player == 1 and piece.type == 1 and piece.y == 7:
                x = piece.x
                y = piece.y
                piece.__init__(5, self.win, x, y)
        for piece in self.pieces:
            if piece.player == 0 and piece.type == 6:
                for piece in self.pieces:
                    if piece.player == 1 and piece.type == 6:
                        return
                self.game_result = 'White won'
                return
        self.game_result = 'Black won'
    
    def draw_game_result(self):
        result = self.font.render(self.game_result, True, (255, 0, 0))
        self.win.blit(result, (180, 220))
    
    def send_move(self, piece, new_pos):
        type = piece.ptype[piece.type]
        fromx, fromy = piece.x, piece.y
        tox, toy = new_pos
        msg = f'{type}|{fromx}|{fromy}|{tox}|{toy}'
        self.socket.send(msg.encode())
    
    def recv_move(self):
        while True:
            msg = self.socket.recv(32).decode()
            print(msg)
            fromx, fromy = msg.split('|')[1:3]
            tox, toy = msg.split('|')[3:]
            for piece in self.pieces:
                if piece.x == int(fromx) and piece.y == int(fromy):
                    self.move_piece(piece, [int(tox), int(toy)])
                    break
