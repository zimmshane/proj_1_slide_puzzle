import random
from collections import deque
from math import sqrt
import heapq

class Node:
    state = tuple()
    move = 0
    def __init__(self,board, move):
        self.state = tuple(board)
        self.move = move

class Tree:
    root = None
    parentDict = {}
    def __init__(self, initState):
        self.root = Node(initState,0)
        self.parentDict[0] = (None,self.root)
        
    def addNode(self,board, currentMove, parentMove):
        newNode = Node(board,currentMove)
        self.parentDict[currentMove] = (parentMove,newNode) 
    
    def findPath(self,winningMove):
        move = winningMove
        count = 1
        print("Calculating an Optimal Solution Path from Search History...")
        while self.parentDict[move][0]:
            parentMove, node = self.parentDict[move]
            print(f"Move: {count}")
            Printer.printState(node.state)
            move = parentMove
            count += 1
        #Loop misses root
        print(f"Move: {count}")
        Printer.printState(self.root.state)
        
           
        
class Puzzle:
    board = []
    moves = 0
    size = 0
    moveTree = None
    winState = [1,2,3,4,5,6,7,8,0]
    quickLookup = [] #qlookup[i] returns (r,c) of i on current sized board
    winFlag = False
    
    #Constructor
    def __init__(self,puzzleType=3):
        self.size = 3
        self.__generateQuickLookup__()
        if puzzleType == 2:
            myboard = input("Enter your puzzle with spaces between the numbers: ").split()
            self.board = [int(x) for x in myboard]
        else:
            self.board = self.getRandomBoard()
        self.moveTree = Tree(self.board)
            
        
    def __generateQuickLookup__(self):
        r , c = 0 , 0
        self.quickLookup=[0]*(self.size**2)
        for i in range(self.size**2):
            self.quickLookup[i]=(r,c)
            if c == self.size - 1:
                c = 0
                r += 1
            else:
                c += 1
                
    
    #Update main board with best move
    def makeMove(self,board,parentMove):
        self.board = board
        self.moves += 1
        self.moveTree.addNode(board,puzzle.moves,parentMove)
        #print(f"Move: {self.moves}")
        #Printer.printState(self.board)
        

        
    #Make a random board config    
    def getRandomBoard(self) -> list:
        print("Creating a random Board")
        board = list(range(self.size**2))
        solvable = False
        while not solvable:
            random.shuffle(board)
            solvable=self.isSolvable(board)
        return board # board
        
        
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
        if (blankIndex + 1) % self.size == 0:
            return None
        right_shift_board = list(self.board)
        right_shift_board[blankIndex],right_shift_board[blankIndex + 1] = right_shift_board[blankIndex + 1],right_shift_board[blankIndex]
        return right_shift_board
  

class Search:
    visited = set()
    moveHeap = []
    hCache = {}  
    cacheMiss = 0
    cacheHit = 0
    searchType = 0
    puzzle = None

    
    def __init__(self, puzzle : Puzzle ,searchType = 0):
        self.puzzle = puzzle
        self.searchType = searchType
        
    
    #coordinate cost calc and return best move
    def findSolution(self) -> bool:
        if puzzle.board == puzzle.winState: return True
        #Misplaced Tile
        visited = set()
        depth = 0
        heapq.heappush(self.moveHeap, (0, puzzle.board, 0)) #( MOVE COST, BOARD, PARENT MOVE)

        while self.moveHeap:
            _  , board , parentMove = heapq.heappop(self.moveHeap)
            puzzle.makeMove(board,parentMove)

            if puzzle.board == puzzle.winState:
                puzzle.winFlag = True
                break
            
            self.__checkAndAdd__(puzzle.getMoveUp(),depth)
            self.__checkAndAdd__(puzzle.getMoveDown(),depth)
            self.__checkAndAdd__(puzzle.getMoveLeft(),depth)
            self.__checkAndAdd__(puzzle.getMoveRight(),depth)
            depth += 1
                
        return puzzle.winFlag
        
        
    def __checkAndAdd__(self,peeker, depth = 0):
        if peeker and (tuple(peeker) not in self.visited):
            self.visited.add(tuple(peeker))
            if self.searchType == 0:
                cost = depth
            elif self.searchType == 1:
                cost = self.__getMisplaceCost__(peeker) + depth
            else:
                cost = self.__getEuclidianCost__(peeker) + depth
            heapq.heappush(self.moveHeap,(cost,peeker.copy(), puzzle.moves))

    
    def __getEuclidianCost__(self, board) -> float:
        totalcost = 0
        for i in range(puzzle.size**2):
            if (puzzle.board[i],i) in self.hCache:
                self.cacheHit += 1
                totalcost += self.hCache[(puzzle.board[i],i)]
                continue
            
            #NOT IN CACHE
            self.cacheMiss += 1
            current_position = self.puzzle.quickLookup[i] #get (x,y)
            desired_position = self.puzzle.quickLookup[self.puzzle.winState.index(self.puzzle.board[i])]
            #calculate euclidian cost
            cost = sqrt((desired_position[0]-current_position[0])**2 + (desired_position[1] - current_position[1])**2)
            #add to cache
            self.hCache[tuple((puzzle.board[i],i))] = cost
            totalcost += cost
            
        return totalcost
    
    def __getMisplaceCost__(self, board) -> int:
        totalCost = 0
        for i in range(puzzle.size**2):
            if puzzle.board[i] != puzzle.winState[i]:
                totalCost += 1
        return totalCost
    
    

class Printer:
    welcome = "Welcome to szimm011 and ladam020 8 puzzle solver"
    config = "Type 1 to get a random board or 2 to configure your own!"
    menu1= """
Enter your choice of algorithm 
0) Uniform Cost Search 
1) A* with the Misplaced Tile heuristic. 
2) A* with the Euclidean distance heuristic.
"""
    
    def __init__(self):
        print(self.welcome)
       
    @staticmethod
    def printState(board : list):
        counter=0
        for i in range(puzzle.size):
            for j in range(puzzle.size):
                print(board[counter],end=" ")
                counter += 1
            print()
        print()
        
    def printSolution(self):
        pass   

#Main
if __name__ == '__main__':
    printer = Printer()
    puzzle = Puzzle(int(input(printer.config)))
    puzzleType = int(input(printer.menu1))
    solver = Search(puzzle, puzzleType)  
    if solver.findSolution():
        puzzle.moveTree.findPath(puzzle.moves)
    print(f"Cache Hits: {solver.cacheHit} Cache Misses: {solver.cacheMiss}")

