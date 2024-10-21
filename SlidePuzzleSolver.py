import random

class Puzzle:
    board = []
    moves = 0
    size = 0
    moveHistory = []
    blankIndex = 0
    
    #Constructor
    def __init__(self):
        puzzleType = input("Type “1” to use a default puzzle, or “2” to enter your own puzzle.")
    
        if puzzleType == 2:
            theInput = input("Enter your puzzle with spaces between the numbers: ")
            theInput.split()
            self.board = theInput
        else:
            self.board = self.getRandomBoard()

        self.size = 3
        self.blankIndex = self.getBlankIndex()
    
    def __getBlankIndex__(self):
        return self.board.index("X")

    #Update main board with best move
    def makeMove(self,board):
        self.board = board
        self.moveHistory.append(board)
        self.moves += 1
        if self.winCondition == self.board:
            print("This is a win!")
        
    #Make a random board config    
    def getRandomBoard(self) -> list: 
        pass
        
    #check if a board config is solvable    
    def isSolvable(self,board:list) -> bool:
        pass
    
    # return board after move up
    def getMoveUp(self) -> list:
        if self.blankIndex >= 0 and self.blankIndex <= self.size:
            return None
        tempBoard = self.board.copy()
        tempBoard[self.blankIndex],tempBoard[self.blankIndex - self.size] = tempBoard[self.blankIndex - self.size],tempBoard[self.blankIndex]
        return tempBoard
    
    # return board after move down
    def getMoveDown(self) -> list:
        if self.blankIndex >= (self.size **2) - self.size and self.blankIndex <= (self.size **2) -1:
            return None
        tempBoard = self.board.copy()
        tempBoard[self.blankIndex],tempBoard[self.blankIndex + self.size] = tempBoard[self.blankIndex + self.size],tempBoard[self.blankIndex]
        return tempBoard
    
    # return board after move left
    def getMoveLeft(self) -> list:
        if self.blankIndex % self.size == 0:
            return None
        tempBoard = self.board.copy()
        tempBoard[self.blankIndex],tempBoard[self.blankIndex - 1] = tempBoard[self.blankIndex - 1],tempBoard[self.blankIndex]
        return tempBoard
    
    # return board after move right
    def getMoveRight(self) -> list:
        if self.blankIndex + 1 % self.size == 0:
            return None
        tempBoard = self.board.copy()
        tempBoard[self.blankIndex],tempBoard[self.blankIndex + 1] = tempBoard[self.blankIndex + 1],tempBoard[self.blankIndex]
        return tempBoard
    

class Search:
    visited = {}
    searchType = 0
    
    def __init__(self,searchType = 0):
        self.searchtype = searchType
    
    #coordinate cost calc and return best move
    def findNextMove(self):
        pass
    
    def getManhattanCost(self, board):
        pass
    
    def getMisplaceCost(self):
        pass
    
    def getUniformCost(self):
        pass
    

class Printer:
    def printState(self,board:list):
        pass
    
    def printMenu(self):
        print("Welcome to szimm011 & ladam020's 8 puzzle solver.")
        
    def printSolution(self):
        pass   

#Main
if __name__ == '__main__':
    printer = Printer()
    puzzle = Puzzle()
    printer.printMenu


    