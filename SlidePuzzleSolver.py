import random
from collections import deque
from math import sqrt

class Puzzle:
    board = []
    moves = 0
    size = 0
    moveHistory = []
    winState = (1,2,3,4,5,6,7,8,0)
    quickLookup = [] #qlookup[i] returns (r,c) of i on current sized board
    winFlag = False

    
    #Constructor
    def __init__(self):
        puzzleType = input("Type “1” to use a default puzzle, or “2” to enter your own puzzle.")
    
        if puzzleType == 2:
            self.board = input("Enter your puzzle with spaces between the numbers: ").split
        else:
            self.board = self.getRandomBoard()
            
        self.size = 3 # size != 3 not yet fully supported
        
    def __generateQuickLookup__(self):
        r , c = 0 , 0
        for i in range(self.size**2 - 1):
            self.quickLookup[i]=(r,c)
            if c == self.size - 1:
                c = 0
                r += 1
            else:
                c += 1

    
    #Update main board with best move
    def makeMove(self,board):
        self.board = board
        self.moveHistory.append(board)
        self.moves += 1

        
    #Make a random board config    
    def getRandomBoard(self) -> set:
        board = list(range(self.size**2 - 1))
        solvable = False
        while not solvable:
            random.shuffle(board)
            solvable=self.isSolvable(board)
        return board
        
        
    #check if a board config is solvable
    # Knowledge Source:
    # https://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable 
    # https://datawookie.dev/blog/2019/04/sliding-puzzle-solvable/  
    def isSolvable(self,board) -> bool:
        inversions = 0
        for i in range(len(board)):
            if board[i] == 0: continue
            for j in range(i,len(board)):
                if board[j] == 0: continue
                if board[i] > board[j]: inversions += 1
        return inversions % 2 == 0
    
    # return board after move up
    def getMoveUp(self) -> list:
        blankIndex = self.board.index(0)
        if blankIndex >= 0 and blankIndex <= self.size:
            return None
        up_Shift_Board = list(self.board)
        up_Shift_Board[blankIndex],up_Shift_Board[blankIndex - self.size] = up_Shift_Board[blankIndex - self.size],up_Shift_Board[blankIndex]
        return up_Shift_Board
    
    # return board after move down
    def getMoveDown(self) -> list:
        blankIndex = self.board.index(0)
        if blankIndex >= (self.size **2) - self.size and blankIndex <= (self.size **2) -1:
            return None
        down_Shift_Board = list(self.board)
        down_Shift_Board[blankIndex],down_Shift_Board[blankIndex + self.size] = down_Shift_Board[blankIndex + self.size],down_Shift_Board[blankIndex]
        return down_Shift_Board
    
    # return board after move left
    def getMoveLeft(self) -> list:
        blankIndex = self.board.index(0)
        if blankIndex % self.size == 0:
            return None
        left_Shift_Board = list(self.board)
        left_Shift_Board[blankIndex],left_Shift_Board[blankIndex - 1] = left_Shift_Board[blankIndex - 1],left_Shift_Board[blankIndex]
        return left_Shift_Board
    
    # return board after move rightdown_
    def getMoveRight(self) -> list:
        blankIndex = self.board.index(0)
        if blankIndex + 1 % self.size == 0:
            return None
        right_shift_board = list(self.board)
        right_shift_board[blankIndex],right_shift_board[blankIndex + 1] = right_shift_board[blankIndex + 1],right_shift_board[blankIndex]
        return right_shift_board
    

class Search:
    visited = {}
    queue = deque()
    hCache = {}  
    searchType = 0
    puzzle = None

    
    def __init__(self, puzzle : Puzzle ,searchType = 0):
        self.puzzle = puzzle
        self.searchtype = searchType
        
    
    #coordinate cost calc and return best move
    def findSolution(self) -> bool:
        if self.searchType == 0:
            #Euclidian
            pass
        elif self.searchType == 1:
            #Misplaced Tile
            pass
        else:
            #Uniform Cost
            self.queue.append(puzzle.board)
            while self.queue:
                
                puzzle.makeMove(self.queue.popleft())
                self.visited[puzzle.board]=puzzle.moves
                
                if puzzle.board == puzzle.winState:
                    puzzle.winFlag = True
                    break
                
                #Look Up
                self.__checkAndAdd__(puzzle.getMoveUp())
                    
                #Look Down
                self.__checkAndAdd__(puzzle.getMoveDown())
                    
                #Look Left
                self.__checkAndAdd__(puzzle.getMoveLeft())
                    
                # Look Right
                self.__checkAndAdd__(puzzle.getMoveRight())
                
        return puzzle.winFlag
                    
                
            
        
        
    def __checkAndAdd__(self,peeker):
        if peeker and peeker not in self.visited:
            self.queue.append(peeker.copy())
    
    def __getEuclidianCost__(self, board):
        totalcost = 0
        for i in range(puzzle.size**2):
            if (puzzle.board[i],i) in self.hCache:
                totalcost += self.hCache[(puzzle.board[i],i)]
                continue
            
            #NOT IN CACHE
            #get (x,y)
            current_position = self.puzzle.quickLookup(i)
            desired_position = self.puzzle.quickLookup(self.puzzle.winState.index(self.puzzle.board[i]))
            #calculate euclidian cost
            cost = sqrt((desired_position[0]-current_position[0])**2 + (desired_position[1] - current_position[1])**2)
            #add to cache
            self.hCache[tuple((puzzle.board[i],i))] = cost
            totalcost += cost
            
        return totalcost
    
    def __getMisplaceCost__(self, board):
        totalCost = 0
        for i in range(puzzle.size**2 - 1):
            if puzzle.board[i] != puzzle.winState[i]:
                totalCost += 1
        return totalCost
    
    

class Printer:
    puzzle = None
    
    def __init__(self,puzzle):
        self.puzzle = puzzle
        
    def printState(self):
        pass
    
    def printMenu(self):
        print("Welcome to szimm011 & ladam020's 8 puzzle solver.")
        
    def printSolution(self):
        pass   

#Main
if __name__ == '__main__':
    printer = Printer()
    puzzle = Puzzle()
    solver = Search(puzzle,0)
    printer.printMenu


    