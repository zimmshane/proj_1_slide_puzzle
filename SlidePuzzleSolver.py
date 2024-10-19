import random

class Puzzle:
    board = []
    moves = 0
    size = set()
    moveHistory = []
    
    #Constructor
    def __init__(self, board:list = None, rows:int = 3, cols:int = 3):
        if board:
            self.board = board
        else:
            self.board = self.getRandomBoard()
            
        self.size = (rows,cols)
    
    #Update main board with best move
    def makeMove(self,board):
        pass
        
    #Make a random board config    
    def getRandomBoard(self) -> list: 
        pass
        
    #check if a board config is solvable    
    def isSolvable(self,board:list) -> bool:
        pass
    
    # return board after move up
    def getMoveUp(self) -> list:
        pass
    
    # return board after move down
    def getMoveDown(self) -> list:
        pass
    
    # return board after move left
    def getMoveLeft(self) -> list:
        pass
    
    # return board after move right
    def getMoveRight(self) -> list:
        pass
        pass
    

class Search:
    visited = {}
    searchType = 0
    
    def __init__(self,searchType = 0):
        self.searchtype = searchType
    
    #coordinate cost calc and return best move
    def findNextMove(self):
        pass
    
    def getManhattanCost(self):
        pass
    
    def getMisplaceCost(self):
        pass
    
    def getUniformCost(self):
        pass
    

class Printer:
    def printState(self,board:list):
        pass
    
    def printMenu(self):
        pass
    
    def printSolution(self):
        pass   

#Main
if __name__ == '__main__':
    pass
    