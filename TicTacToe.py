import pygame
import sys

class Board:
    
    def __init__(self, game):
        self.LINE_COLOR = (240,230,140)
        self.LINE_THICKNESS = 2
        self.SURFACE_BACKGROUND = (0, 0, 0)
        pygame.init()
        self.font = pygame.font.Font(None, 24)
        self.game = game
        self.GUI = pygame.display.set_mode((450, 450))
        self.winner = None
        self.currentPlayer = 'H'    #H for Human, C for Computer
        pygame.display.set_caption('Tic Tac Toe')
        self.currentDisplayedMessage = None
        self.GUI.fill(self.SURFACE_BACKGROUND)
        pygame.draw.line(self.GUI, self.LINE_COLOR, (150, 0),(150, 425), self.LINE_THICKNESS)
        pygame.draw.line(self.GUI, self.LINE_COLOR, (300, 0),(300, 425), self.LINE_THICKNESS)
        pygame.draw.line(self.GUI, self.LINE_COLOR, (0, 150),(450, 150), self.LINE_THICKNESS)
        pygame.draw.line(self.GUI, self.LINE_COLOR, (0, 300),(450, 300), self.LINE_THICKNESS)
        pygame.display.update()
     
     
    
    def __fillCell__(self, row, col):
        if self.game.is_complete():
            return
        
        idx = 3 * row + col
        
        if self.game.state[idx] is not '-':
            return

        fillChar = "O" if self.currentPlayer is 'H' else "X" 
        self.game.state = self.game.state[:idx] + fillChar + self.game.state[idx + 1:] 
        
        
        cx = col * 150 + 75
        cy = row * 150 + 75

        # draw the appropriate piece
        if self.currentPlayer is 'H':
            pygame.draw.circle (self.GUI, self.LINE_COLOR, (cx, cy), 30, 4)
            self.currentPlayer = 'C'
        else:
            pygame.draw.line (self.GUI, self.LINE_COLOR, (cx - 25, cy - 25), \
                         (cx + 25, cy + 25), 4)
            pygame.draw.line (self.GUI, self.LINE_COLOR, (cx + 25, cy - 25), \
                         (cx - 25, cy + 25), 4)
            self.currentPlayer = 'H'
        self.updateStatusBar()
        pygame.display.update()
        
        if self.currentPlayer is 'C':
            print('Calling Minimax')
            nextIdx, _ = minimax(self.game, True, idx)
            self.__fillCell__(nextIdx / 3, nextIdx % 3)
            print(nextIdx)
    #
    #
    #
    def fillCell(self, xCord, yCord):        
        row = 0 if yCord < 150 else 1 if yCord < 300 else 2
        col = 0 if xCord < 150 else 1 if xCord < 300 else 2
        self.__fillCell__(row, col)
 
                    
    def updateStatusBar(self):
        if self.game.is_complete():            
            score = self.game.score()
            self.winner  = 'H' if score == -10 else 'C' if score == 10 else 'T'
            
        if self.winner is None:            
            message = 'Click an empty cell to play your turn' if self.currentPlayer is 'H' else 'Please wait, computer working on its move...' 
        else:
            message = 'You won' if self.winner is 'H' else 'You lost' if self.winner is 'C' else 'Game tied'
          
        
        if self.currentDisplayedMessage is not None:
            text = self.font.render(self.currentDisplayedMessage, 1, self.SURFACE_BACKGROUND)
            self.GUI.blit(text, (10, 430))
            pygame.display.update()
        
        
        text = self.font.render(message, 1, (70, 130, 180))
        self.GUI.blit(text, (10, 430))
        pygame.display.update()
        self.currentDisplayedMessage = message
        
    def startGame(self):
        self.currentPlayer = 'H'
        self.updateStatusBar()
        self.waitForEvent()
        


    def waitForEvent(self):        
        while True:
            event = pygame.event.wait()
            if event.type is pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type is pygame.MOUSEBUTTONUP:
                mouseX, mouseY = pygame.mouse.get_pos()
                self.fillCell(mouseX, mouseY)
                   

class Game:
    
    def __init__(self, state):
        #State is a string of 9 chars with X, O or -
        self.state = state
        self.winning_positions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    def get_empty_slots(self):
        return [c is '-' for c in self.state]
    
    
    
    # isSelf flag determines whether we put X or O in the empty slots
    def get_available_moves(self, isSelf):
        char_to_fill = 'X' if isSelf else 'O'
        available_slots = self.get_empty_slots()
        return [(i, self.state[:i] + char_to_fill + self.state[i + 1:]) for i in range(0, 9) if available_slots[i]]


    def with_state(self, state):
        return Game(state)


    def score(self):
        is_x_winning_any =  [[self.state[c] is 'X' for c in x] for x in self.winning_positions]
        if any([all(c) for c in is_x_winning_any]):
            return 10

        is_o_winning_any =  [[self.state[c] is 'O' for c in x] for x in self.winning_positions]
        if any([all(c) for c in is_o_winning_any]):
            return -10

        return 0


    #
    #
    #
    def is_complete(self):
        sc = self.score()
        return (not any(self.get_empty_slots())) or sc == 10 or sc == -10
    
    
    

#
#   The game object is expected to have the functions
#        1. get_available_moves(isSelf): which returns list of available moves, these are also called new game states
#        2. with_state, returns a new game instance given a state
#        3. is_complete: tests if the game is complete
#        4. score()
#
#    returns  (next_move, expected score)
#
def minimax(game, isMaximizing, lastMoveIndex = 0, depth = 0):
    bestScore = -20 if isMaximizing else 20
    score = game.score()

    if game.is_complete():
        return (lastMoveIndex, score + depth) if isMaximizing else (lastMoveIndex, score - depth) 
    
    moves = game.get_available_moves(isMaximizing)
    bestMove = None
    for i, move in moves:
        currGame = Game(move)
        if isMaximizing:        
            _, score = minimax(currGame, not isMaximizing, i, depth + 1)
            if score > bestScore:
                bestScore = score
                bestMove = i
        else:        
            _, score = minimax(currGame, not isMaximizing, i, depth + 1)
            if score < bestScore:
                bestScore = score
                bestMove = i
    
    return (bestMove, bestScore)



if __name__ == '__main__':
    
    initial_state = '-' * 9
    game =Game(initial_state)
    board = Board(game)
    board.startGame()
    #game =Game('XOXOXO--O')
    #print(minimax(game, True))



