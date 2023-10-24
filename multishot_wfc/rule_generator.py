# generate rules based on .png image
# generated rules have the predicates
#   legal((DX, DY), P1, P2)
#   offset(DX, DY)
#   pattern(P)
#   pattern_weight(P, N)

import numpy as np
import matplotlib.pyplot as plt
import sys

class Rule:
    def __init__(self, base, neighbour, dir):
        self.base = tuple(int(k*255) for k in base)
        self.neighbour = tuple(int(k*255) for k in neighbour)
        self.dir = dir
    
    def __repr__(self) -> str:
        return f"legal(({self.dir[0]}, {self.dir[1]}), {self.base}, {self.neighbour})."
    
    def __hash__(self):
        return hash(self.__repr__())
    
    def __eq__(self, other):
        return (isinstance(other, Rule) and
                (self.base == other.base) and 
                (self.neighbour == other.neighbour) and 
                (self.dir == other.dir))

file_path = sys.argv[1]
# img = plt.imread("input/red_maze.png")
img = plt.imread(file_path)

rules = set()
patterns = {}

width = img.shape[0]
height = img.shape[1]

for j in range(height):
    for i in range(width):

        col = tuple(int(k*255) for k in img[i][j])
        if col not in patterns: patterns[col] = 1
        else: patterns[col] += 1

        if i - 1 >= 0:
            rules.add(Rule(img[i][j], img[i-1][j], (0, -1)))
        if i + 1 < width:
            rules.add(Rule(img[i][j], img[i+1][j], (0, 1)))
        if j - 1 >= 0:
            rules.add(Rule(img[i][j], img[i][j-1], (-1, 0)))
        if j + 1 < height:
            rules.add(Rule(img[i][j], img[i][j+1], (1, 0)))

        # for k in range(-1, 2):
        #     for l in range(-1, 2):
        #         if k == 0 and l == 0: continue
        #         dx = (i+k)%width
        #         dy = (j+l)%height
        #         # print((i, j), (dx, dy), (k, l), width, height)
        #         rules.add(Rule(img[i][j], img[dx][dy], (k, l)))


file_name = file_path.split("/")[-1][:-4]
f = open(f"{file_name}_rules.lp", "w")

output = "#program rules.\n"
output += "\n".join(map(lambda rule: rule.__repr__(), rules))
output += "\n\noffset(1, 0)."
output += "\noffset(-1, 0)."
output += "\noffset(0, 1)."
output += "\noffset(0, -1)."
output += "\n\n" + "\n".join([f"pattern({s})." for s in patterns.keys()])
output += "\n\n" + "\n".join([f"pattern_weight({k}, {v})." for (k, v) in patterns.items()])

print(output)

f.write(output)
f.close()