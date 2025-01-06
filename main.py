from cube import Node, Puzzle
from copy import deepcopy
import graphviz

COLORS = "abcdefghijklmnopqrstuvwxyz"
world = set()

def CreateEmptyPuzzle(size):
    return Puzzle([[Node((i, j)) for j in range(size)] for i in range(size)])

def SetPuzzleToResolved(puzzle:Puzzle):
    """
    Sets the puzzle to a resolved state in place
    """
    for i in range(len(puzzle.matrix)):
        for j in range(len(puzzle.matrix)):
            puzzle.matrix[i][j].color = COLORS[i]

def ShowCurrentPuzzleState(puzzle:Puzzle):
    """
    Prints puzzle to standard output
    """
    for ligne in puzzle.matrix:
        line = ""
        for element in ligne:
            line += f"{element.color} " 
        print(line)

def GetCurrentStateAsString(puzzle:Puzzle) -> str:
    rep = ""
    for ligne in puzzle.matrix:
        line = ""
        for element in ligne:
            line += f"{element.color} " 
        rep += f"{line}\n"
    return rep[:-2]

def Move(puzzle:Puzzle, fromWhere:int, up:bool|None=None, left:bool|None=False):
    match up:
        case True:
            firstNode = puzzle.matrix[0][fromWhere]
            for i in range(len(puzzle.matrix)-1):
                puzzle.matrix[i][fromWhere] = puzzle.matrix[i+1][fromWhere]
            puzzle.matrix[len(puzzle.matrix)-1][fromWhere] = firstNode
        case False:
            lastNode = puzzle.matrix[len(puzzle.matrix)-1][fromWhere]
            for i in range(len(puzzle.matrix)-1, 0, -1):
                puzzle.matrix[i][fromWhere] = puzzle.matrix[i-1][fromWhere]
            puzzle.matrix[0][fromWhere] = lastNode
        case None:
            match left:
                case False:
                    firstNode = puzzle.matrix[fromWhere][0]
                    for i in range(len(puzzle.matrix)-1):
                        puzzle.matrix[fromWhere][i] = puzzle.matrix[fromWhere][i+1]
                    puzzle.matrix[fromWhere][len(puzzle.matrix)-1] = firstNode

                case True:
                    lastNode = puzzle.matrix[fromWhere][len(puzzle.matrix)-1]
                    for i in range(len(puzzle.matrix)-1, 0, -1):
                        puzzle.matrix[fromWhere][i] = puzzle.matrix[fromWhere][i-1]
                    puzzle.matrix[fromWhere][0] = lastNode

def GetCurrentState(puzzle:Puzzle):
    return deepcopy(puzzle.matrix)

def CreatePossibleMoves(puzzle:Puzzle):
    rep = []
    for i in range(len(puzzle.matrix)):
        rep.append((i, True)) #Haut
        rep.append((i, False))#Bas
        rep.append((i, None, True)) #Gauche
        rep.append((i, None, False))#Droite
    return rep

def AddStatesToGraphe(puzzle:Puzzle, predecessor:Puzzle, file, depth):    
    global world
    
    world.add(puzzle)

    file.write(f'"{GetCurrentStateAsString(predecessor)}" -- "{GetCurrentStateAsString(puzzle)}";\n')

    if depth <= 1:
        return
    
    for move in CreatePossibleMoves(puzzle):
        newState = deepcopy(puzzle)
        Move(newState, *move)
        if newState not in world:
            AddStatesToGraphe(newState, puzzle, file, depth-1)


def CreateGraphOfMoves(puzzle:Puzzle, file, depth:int):
    global world
    world = set()
    file.write("strict graph {\n")
    AddStatesToGraphe(puzzle, puzzle, file, depth)

    file.write("\n}")

def test():
    with open("dot.dot", "w") as dotFile:
        puzzle = CreateEmptyPuzzle(3)
        SetPuzzleToResolved(puzzle)
        CreateGraphOfMoves(puzzle, dotFile, 6)

    graphviz.render("dot", "svg", "dot.dot")

if __name__ == "__main__":

    """rubik = CreateEmptyPuzzle(5)
    SetPuzzleToResolved(rubik)
    ShowCurrentPuzzleState(rubik)
    print()
    Move(rubik, 0, True)
    ShowCurrentPuzzleState(rubik)
    Move(rubik, 0, None, False)
    print()
    ShowCurrentPuzzleState(rubik)"""

    test()