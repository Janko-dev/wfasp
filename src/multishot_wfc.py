import sys
from typing import Sequence
from clingo.application import Application, clingo_main
from clingo.control import Control
from clingo.symbol import Number, Function
from clingo.solving import Model

import random
import math

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap 

class WFC(Application):
    program_name = "WaveFunctionCollapse"
    version = "1.0"

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._x = 0
        self._y = 0
        self._p = ""
        self._t = 0

    def get_least_entropy(self, model):

        least_entropy = []
        for atom in model.symbols(atoms=True):
            if atom.match("least_entropy", 4) and atom.arguments[3].number == self._t:
                # print("TEST", atom)
                # least_entropy.append((atom.arguments[0].number, atom.arguments[1].number, atom.arguments[2].name))
                # pattern = [p.name for p in atom.arguments[2].arguments]
                least_entropy.append((atom.arguments[0].number, atom.arguments[1].number, atom.arguments[2].arguments))
        
        # print(least_entropy)
        if len(least_entropy) == 0: return

        (x, y, p) = random.choice(least_entropy)
        self._x = x
        self._y = y
        self._p = p
    
    def main(self, prg: Control, files: Sequence[str]):

        for file in files:
            prg.load(file)
        
        iters = int((self.width)*(self.height))

        prg.ground([("rules", [])])

        prg.ground([("base", [
            Number(self.height), 
            Number(self.width), 
            Number(iters-1)
        ])])
        
        # initialize
        # prg.assign_external(
        #     Function("assigned", [
        #         Number(2), Number(1),
        #         Function("b"), Number(0)
        #     ]), True)

        prg.assign_external(
            Function("assigned", [
                Number(1), 
                Number(1),
                Function("", [
                    Function("", [Function("a"), Function("a")]), 
                    Function("", [Function("a"), Function("b")])
                ]), 
                Number(0)
            ]), True)
        
        # iteration
        for i in range(1, iters):

            self._t = i

            prg.ground([("step", [Number(i)])])
            
            prg.solve(on_model=self.get_least_entropy)

            print(self._x, self._y, self._p, i)

            # return
            prg.assign_external(
                Function("assigned", [
                    Number(self._x), Number(self._y),
                    Function("", self._p), Number(i)
                ]), True)
        
        
        prg.solve(on_model=self.visualize)

    def visualize(self, model: Model):
        colors = {
            "a": [1., 1., 1.], 
            "b": [0., 0., 0.], 
            "c": [1, 0., 0.]
        }
        
        SCALE = 100
        grid = np.zeros((self.width*SCALE, self.height*SCALE, 3))

        for atom in model.symbols(shown=True):
            x = atom.arguments[0].number - 1
            y = atom.arguments[1].number - 1
            p1, p2 = atom.arguments[2].arguments
            p1a, p1b = p1.arguments
            p2a, p2b = p2.arguments
            
            grid[y*SCALE:(y+1)*SCALE, x*SCALE:(x+1)*SCALE, :] = colors[p1a.name]
            grid[y*SCALE:(y+1)*SCALE, (x+1)*SCALE:(x+2)*SCALE, :] = colors[p1b.name]
            grid[(y+1)*SCALE:(y+2)*SCALE, x*SCALE:(x+1)*SCALE, :] = colors[p2a.name]
            grid[(y+1)*SCALE:(y+2)*SCALE, (x+1)*SCALE:(x+2)*SCALE, :] = colors[p2b.name]


        # plt.imshow(grid)
        # plt.show()
        plt.imsave("img.png", grid)

# clingo_args = ["0", "--outf=3"]
clingo_args = ["0"]

clingo_main(WFC(6, 6), sys.argv[1:] + clingo_args)

