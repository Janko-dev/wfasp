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
                
                # self._r = atom.arguments[0].number
                # self._c = atom.arguments[1].number
                # self._s = atom.arguments[2].name
                # return
                least_entropy.append((atom.arguments[0].number, atom.arguments[1].number, atom.arguments[2].name))
        
        if len(least_entropy) == 0: return

        (x, y, p) = random.choice(least_entropy)
        self._x = x
        self._y = y
        self._p = p
    
    def main(self, prg: Control, files: Sequence[str]):

        for file in files:
            prg.load(file)
        
        iters = self.width*self.height

        prg.ground([("base", [
            Number(self.height), 
            Number(self.width), 
            Number(iters-1)
        ])])
        
        # initialize
        prg.assign_external(
            Function("assigned", [
                Number(2), Number(2),
                Function("c"), Number(0)
            ]), True)
        
        # iteration
        for i in range(1, iters):

            self._t = i

            prg.ground([("step", [Number(i)])])
            
            prg.solve(on_model=self.get_least_entropy)

            print(self._x, self._y, self._p, i)

            prg.assign_external(
                Function("assigned", [
                    Number(self._x), Number(self._y),
                    Function(self._p), Number(i)
                ]), True)
        
        
        prg.solve(on_model=self.visualize)

    def visualize(self, model: Model):
        colors = {
            "a": [0., 0., 0.], 
            "b": [1., 1., 1.], 
            "c": [1, 0., 0.]
        }
        
        SCALE = 100
        grid = np.zeros((self.width*SCALE, self.height*SCALE, 3))

        for atom in model.symbols(shown=True):
            x = atom.arguments[0].number - 1
            y = atom.arguments[1].number - 1
            p = atom.arguments[2].name
            grid[x*SCALE:(x+1)*SCALE, y*SCALE:(y+1)*SCALE, :] = colors[p]

        # print(grid)
        plt.imsave("img.png", grid)

clingo_main(WFC(5, 5), sys.argv[1:] + ["0"])

