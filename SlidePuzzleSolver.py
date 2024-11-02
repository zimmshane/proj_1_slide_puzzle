import random
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
        print("Calculating an Optimal Path from Search Tree...")
        while self.parentDict[move][0]:
            parentMove, node = self.parentDict[move]
            print(f"Move: {count}")
            Printer.printState(node.state)
            move = parentMove
            count += 1
        #Loop misses root so we add it to the end
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
    errorFlag = False
    
    #Constructor
    def __init__(self,puzzleType=3):
        self.size = 3
        self.__generateQuickLookup__()
        if puzzleType == 2:
            myboard = input("Enter your puzzle with spaces between the numbers: ").split()
            self.board = [int(x) for x in myboard]
        else:
            print("Generating a Random Board...")
            self.board = self.getRandomBoard()
            print("Random Board:")
            Printer.printState(self.board)
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
        
    #Make a random board config    
    def getRandomBoard(self) -> list:
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
    cacheTracker = [0,0] #[CACHE HITS, CACHE MISS]
    maxHeapSize = 1
    searchType = 0
    showAllMoves = False
    puzzle = None
    
    def __init__(self, puzzle , showAllMoves= False, searchType = 0,):
        self.puzzle = puzzle
        self.searchType = searchType
        self.showAllMoves = showAllMoves
        
    #coordinate cost calc and return best move
    def findSolution(self) -> bool:
        print("Searching for a Solution... ",end="")
        if puzzle.errorFlag: return False
        
        heapq.heappush(self.moveHeap, (0, puzzle.board, 0)) #( MOVE COST, BOARD, PARENT MOVE)

        while self.moveHeap and not puzzle.winFlag:
            tCost  , board , parentMove = heapq.heappop(self.moveHeap)
            puzzle.makeMove(board,parentMove)

            if self.showAllMoves:
                print(f"Move: {puzzle.moves} | Cost: {tCost} | g(n) = {parentMove} | h(n) = {tCost-parentMove}")
                Printer.printState(puzzle.board)
                
            if puzzle.board == puzzle.winState:
                puzzle.winFlag = True
                break
            
            self.__checkAndAdd__(puzzle.getMoveUp()) #Look Up
            self.__checkAndAdd__(puzzle.getMoveDown()) #Look Down
            self.__checkAndAdd__(puzzle.getMoveLeft()) #Look Left
            self.__checkAndAdd__(puzzle.getMoveRight()) #Look Right
            self.maxHeapSize = max(self.maxHeapSize,len(self.moveHeap))
            
        if puzzle.winFlag:
            print("Solution Found!")
        else:
            print("No Solution!")       
        return puzzle.winFlag
         
    def __checkAndAdd__(self,peekAhead):
        if peekAhead == puzzle.winState: #State is winner, immediatly make move
            puzzle.makeMove(peekAhead,puzzle.moves)
            puzzle.winFlag = True
            return
        if peekAhead and (tuple(peekAhead) not in self.visited):
            cost = 0
            self.visited.add(tuple(peekAhead))
            if self.searchType == 0:
                cost = puzzle.moves
            elif self.searchType == 1:
                cost = self.__getMisplaceCost__(peekAhead) + puzzle.moves
            else:
                cost = self.__getEuclidianCost__(peekAhead) + puzzle.moves
            heapq.heappush(self.moveHeap,(cost, peekAhead.copy(), puzzle.moves))

    
    def __getEuclidianCost__(self, board) -> float:
        totalcost = 0
        for i, tile in enumerate(board):
            if tile == 0:  # Skip the blank tile
                continue
            if (tile, i) in self.hCache:
                self.cacheTracker[0] += 1
                totalcost += self.hCache[(tile, i)]
                continue

            #NOT IN CACHE
            self.cacheTracker[1] += 1
            current_position = self.puzzle.quickLookup[i]  # get (x,y)
            desired_position = self.puzzle.quickLookup[tile - 1]  # -1 because tiles are 1-indexed
            #calculate euclidian cost
            cost = sqrt((desired_position[0]-current_position[0])**2 + (desired_position[1] - current_position[1])**2)
            #add to cache
            self.hCache[(tile, i)] = cost
            totalcost += cost

            
        return totalcost
    
    def __getMisplaceCost__(self, board) -> int:
        totalCost = 0
        for i in range(puzzle.size**2):
            if board[i] == 0: continue
            if board[i] != puzzle.winState[i]:
                totalCost += 1
        return totalCost
    
    

class Printer:
    welcome = "Welcome to szimm011 and ladam020 8 puzzle solver"
    config = "Type 1 to get a random board or 2 to configure your own: "
    menu1= """Enter your choice of algorithm 
0) Uniform Cost Search 
1) A* with the Misplaced Tile heuristic. 
2) A* with the Euclidean distance heuristic.
Input: """
    showMoves = "Show All States? (y/n): "
    puzzle = None
    
    @staticmethod
    def printWelcome():
        print(Printer.welcome)
        
    @staticmethod
    def printState(board : list, size = 3):
        counter=0
        for i in range(size):
            for j in range(size):
                print(board[counter],end=" ")
                counter += 1
            print()
        print()
        
    @staticmethod
    def printStats(puzzle,solver):
        print(f"Cache HIT / MISS: {solver.cacheTracker}")
        print(f"States Examined: {puzzle.moves}")
        print(f"Max Heap Size: {solver.maxHeapSize}")
        
    @staticmethod
    def printMenu():
        return input(Printer.menu1)
    
    @staticmethod
    def boardConfig() -> int:
        return int(input(Printer.config))
       
    @staticmethod
    def showAllMoves() -> bool:
        showMoves = input(Printer.showMoves).lower()
        if showMoves == "y":
            return True
        else:
            return False

#Main
if __name__ == '__main__':
    Printer.printWelcome()
    puzzle = Puzzle(Printer.boardConfig())
    printer = Printer()
    if puzzle.errorFlag:
        exit(-1)
    #Show all puzzle
    solver = Search(puzzle,Printer.showAllMoves(), int(Printer.printMenu()))  
    if solver.findSolution():
        puzzle.moveTree.findPath(puzzle.moves)
    Printer.printStats(puzzle,solver)
