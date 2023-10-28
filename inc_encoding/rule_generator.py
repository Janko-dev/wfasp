# generate rules based on .png image
# generated rules have the predicates
#   legal((DX, DY), P1, P2)
#   offset(DX, DY)
#   pattern(P)
#   pattern_weight(P, N)

import numpy as np
import matplotlib.pyplot as plt
import argparse

class Rule:
    def __init__(self, base, neighbour, dir):
        self.base = base
        self.neighbour = tuple(tuple(tuple(int(m*255) for m in k) for k in l) for l in neighbour)
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

def generate_rules(file_path, n):

    # file_path = sys.argv[1]
    # img = plt.imread("input/red_maze.png")
    img = plt.imread(file_path)

    rules = set()
    patterns = {}

    width = img.shape[0]
    height = img.shape[1]

    # for j in range(height):
    #     for i in range(width):

    #         col = tuple(int(k*255) for k in img[i][j])
    #         if col not in patterns: patterns[col] = 1
    #         else: patterns[col] += 1

    #         if i - 1 >= 0:
    #             rules.add(Rule(img[i][j], img[i-1][j], (0, -1)))
    #         if i + 1 < width:
    #             rules.add(Rule(img[i][j], img[i+1][j], (0, 1)))
    #         if j - 1 >= 0:
    #             rules.add(Rule(img[i][j], img[i][j-1], (-1, 0)))
    #         if j + 1 < height:
    #             rules.add(Rule(img[i][j], img[i][j+1], (1, 0)))

            # for k in range(-1, 2):
            #     for l in range(-1, 2):
            #         if k == 0 and l == 0: continue
            #         dx = (i+k)%width
            #         dy = (j+l)%height
            #         # print((i, j), (dx, dy), (k, l), width, height)
            #         rules.add(Rule(img[i][j], img[dx][dy], (k, l)))

    for j in range(0, height, n):
        for i in range(0, width, n):
            win = img[i:i+n, j:j+n]
            if win.shape[0] != n or win.shape[1] != n: continue
            
            pat = tuple(tuple(tuple(int(m*255) for m in k) for k in l) for l in win)
            if pat not in patterns: patterns[pat] = 1
            else: patterns[pat] += 1

            if i - n >= 0:
                nbr = img[i-n:i, j:j+n]
                if nbr.shape[0] != n or nbr.shape[1] != n: continue
                rules.add(Rule(pat, nbr, (0, -1)))
            if i + n < width:
                nbr = img[i+n:i+2*n, j:j+n]
                if nbr.shape[0] != n or nbr.shape[1] != n: continue
                rules.add(Rule(pat, nbr, (0, 1)))
            if j - n >= 0:
                nbr = img[i:i+n, j-n:j]
                if nbr.shape[0] != n or nbr.shape[1] != n: continue
                rules.add(Rule(pat, nbr, (-1, 0)))
            if j + n < height:
                nbr = img[i:i+n, j+n:j+2*n]
                if nbr.shape[0] != n or nbr.shape[1] != n: continue
                rules.add(Rule(pat, nbr, (1, 0)))

    file_name = file_path.split("/")[-1][:-4]
    f = open(f"{file_name}_rules.lp", "w")

    output = "#program rules.\n"
    output += "\n".join(map(lambda rule: rule.__repr__(), rules))
    output += f"\n\noffset(1, 0)."
    output += f"\noffset(-1, 0)."
    output += f"\noffset(0, 1)."
    output += f"\noffset(0, -1)."
    output += "\n\n" + "\n".join([f"pattern({s})." for s in patterns.keys()])
    output += "\n\n" + "\n".join([f"pattern_weight({k}, {v})." for (k, v) in patterns.items()])

    print(output)

    f.write(output)
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rule generator based on example .png image')
    parser.add_argument('file_path', type=str, help='file_path to .png file')
    parser.add_argument('-n', type=int, help='number of patterns in NxN square to consider')
    args = parser.parse_args()
    # print(args.file_path)
    # print(args.n)
    generate_rules(args.file_path, args.n)