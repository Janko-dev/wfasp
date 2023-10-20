import sys
from typing import Sequence
from clingo import Symbol
from clingo.application import Application, clingo_main
from clingo.control import Control
from clingo.symbol import Number, Function
from clingo.solving import Model
from cProfile import Profile
from pstats import SortKey, Stats

import random

import numpy as np
import matplotlib.pyplot as plt

SCALE = 128
FILE_PATH = "simple_tiles/"

class WFC(Application):
    program_name = "Tiled Wave Function Collapse (TWFC) with Dynamic system"
    version = "1.0"

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._x = 0
        self._y = 0
        self._p = None
        self._t = 0

    def get_least_entropy(self, model: Model):

        grid = np.zeros((self.height*SCALE, self.width*SCALE, 4))

        least_entropy = []
        for atom in model.symbols(atoms=True):
            
            if atom.match("least_entropy", 2):
                least_entropy.append((atom.arguments[0].arguments, atom.arguments[1].arguments))
            
            write_tile_to_buf(atom, grid, FILE_PATH, SCALE)
        

        plt.imsave(f"process/img{self._t}.png", grid)
        if len(least_entropy) == 0: return

        ((x, y), p) = random.choice(least_entropy)
        self._x = x.number
        self._y = y.number
        self._p = p
    
    def main(self, prg: Control, files: Sequence[str]):

        for file in files:
            prg.load(file)
        
        prg.ground([("rules", [])])

        prg.ground([("base", [
            Number(self.height), 
            Number(self.width)
        ])])

        prg.ground([("input", [])])

        # iteration
        for i in range(0, self.width*self.height):

            self._t = i
            
            prg.solve(on_model=self.get_least_entropy)
            
            print(self._x, self._y, self._p, i)

            forced_assignment = Function("force", [
                    Number(self._x), Number(self._y),
                    Function("", self._p)
                ])

            prg.assign_external(forced_assignment, True)
        
        
        prg.solve(on_model=self.visualize)

    def visualize(self, model: Model):
        
        grid = np.zeros((self.height*SCALE, self.width*SCALE, 4))

        for atom in model.symbols(atoms=True):
            write_tile_to_buf(atom, grid, FILE_PATH, SCALE)

        plt.imsave("img.png", grid)


def write_tile_to_buf(atom: Symbol, grid: np.ndarray, folder_path: str, scale: int):
    if atom.match("assigned", 2): 
        (x, y) = atom.arguments[0].arguments
        x = x.number - 1
        y = y.number - 1
        tile_name, rot = atom.arguments[1].arguments
        
        tile = plt.imread(folder_path+tile_name.name+".png")
        tile = np.rot90(tile, rot.number)

        grid[y*scale:(y+1)*scale, x*scale:(x+1)*scale, :] = tile

clingo_args = ["0", "--outf=3"]
# clingo_args = ["0"]

with Profile() as profile:
    clingo_main(WFC(5, 5), sys.argv[1:] + clingo_args)
    (
        Stats(profile)
        .strip_dirs()
        .sort_stats("tottime")
        .print_stats(10)
    )

