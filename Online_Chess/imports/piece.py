import pygame

class Piece():
    def __init__(self, type, win, x, y):
        self.ptype = {
            1: 'pawn', 2: 'rook',
            3: 'knight', 4: 'bishop',
            5: 'queen', 6: 'king'
        }
        self.win = win
        self.player = 0 if type < 0 else 1
        self.type = abs(type)
        self.first_time = True
        self.ico_orig = pygame.image.load(f'imgs/{str(self.player)}{self.ptype[self.type]}.png')
        self.ico = pygame.transform.scale(self.ico_orig, (64, 64))
        self.x = x
        self.y = y
    
    def show(self):
        self.win.blit(self.ico, (self.x*64, self.y*64))
    
    def get_valid_moves(self, board):
        self.valid_moves = []
        if self.type == 1:
            if self.player == 0:
                if self.inbound(self.x+1, self.y-1):
                    if board[self.y-1][self.x+1] > 0:
                        self.valid_moves.append([self.x+1, self.y-1])
                if self.inbound(self.x-1, self.y-1):
                    if board[self.y-1][self.x-1] > 0:
                        self.valid_moves.append([self.x-1, self.y-1])
                if self.first_time:
                    self.traverse(board, [0, -1], 2, step=False)
                else:
                    self.traverse(board, [0, -1], 1, step=False)
            if self.player == 1:
                if self.inbound(self.x+1, self.y+1):
                    if board[self.y+1][self.x+1] < 0:
                        self.valid_moves.append([self.x+1, self.y+1])
                if self.inbound(self.x-1, self.y+1):
                    if board[self.y+1][self.x-1] < 0:
                        self.valid_moves.append([self.x-1, self.y+1])
                if self.first_time:
                    self.traverse(board, [0, 1], 2, step=False)
                else:
                    self.traverse(board, [0, 1], 1, step=False)
        elif self.type == 2:
            for i in [-1, 1]:
                self.traverse(board, [0, i], 7)
                self.traverse(board, [i, 0], 7)
        elif self.type == 3:
            for i in [-2, 2]:
                for j in [-1, 1]:
                    if self.inbound(self.x+i, self.y+j):
                        if (self.player == 0 and board[self.y+j][self.x+i] >= 0) or (self.player == 1 and board[self.y+j][self.x+i] <= 0):
                            self.valid_moves.append([self.x+i, self.y+j])
                    if self.inbound(self.x+j, self.y+i):
                        if (self.player == 0 and board[self.y+i][self.x+j] >= 0) or (self.player == 1 and board[self.y+i][self.x+j] <= 0):
                            self.valid_moves.append([self.x+j, self.y+i])
        elif self.type == 4:
            for i in [-1, 1]:
                self.traverse(board, [i, i], 7)
                self.traverse(board, [i, -i], 7)
        elif self.type == 5:
            for i in [-1, 1]:
                self.traverse(board, [0, i], 7)
                self.traverse(board, [i, 0], 7)
                self.traverse(board, [i, i], 7)
                self.traverse(board, [i, -i], 7)
        elif self.type == 6:
            for i in [-1, 1]:
                self.traverse(board, [0, i], 1)
                self.traverse(board, [i, 0], 1)
                self.traverse(board, [i, i], 1)
                self.traverse(board, [i, -i], 1)
        return self.valid_moves
    
    def traverse(self, board, direc, max_steps, step=True):
        pos = [self.x, self.y]
        for i in range(max_steps):
            pos[0] += direc[0]
            pos[1] += direc[1]
            if not self.inbound(pos[0], pos[1]):
                break
            elif board[pos[1]][pos[0]] != 0:
                if step:
                    if (self.player == 0 and board[pos[1]][pos[0]] > 0) or (self.player == 1 and board[pos[1]][pos[0]] < 0):
                        self.valid_moves.append([pos[0], pos[1]])
                break
            else:
                self.valid_moves.append([pos[0], pos[1]])
    
    def inbound(self, posX, posY):
        if posX > 7 or posX < 0 or posY > 7 or posY < 0:
            return False
        return True
