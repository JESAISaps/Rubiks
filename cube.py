from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class Node:
    pos:tuple[int, int]
    color:None|str=""

@dataclass()
class Puzzle:
    matrix:list[list[Node]]

    def __hash__(self):
        rep = ""
        for ligne in self.matrix:
            for node in ligne:
                rep += node.color
        return hash(rep)
