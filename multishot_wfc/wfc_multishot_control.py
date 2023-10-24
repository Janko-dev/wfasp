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
    program_name = "Tiled Wave Function Collapse (TWFC)"
    version = "1.0"

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._x = 0
        self._y = 0
        self._p = None
        self._t = 0
        self.DEBUG = True

    def analyse_model(self, model: Model):

        if self.DEBUG:
            grid = np.zeros((self.height*SCALE, self.width*SCALE, 4))
            counts = {}

        lowest_entropy = []
        p_weights = []
        for atom in model.symbols(atoms=True):
            
            if atom.match("lowest_entropy", 3):
                lowest_entropy.append((atom.arguments[0].arguments, atom.arguments[1].arguments))
                p_weights.append(atom.arguments[2].number)
            
            if self.DEBUG:
                write_tile_to_buf(atom, grid, FILE_PATH, SCALE)

                if atom.match("superpos", 2):
                    (x, y) = atom.arguments[0].arguments
                    x = x.number - 1
                    y = y.number - 1

                    if (x, y) not in counts: counts[(x, y)] = 1
                    else: counts[(x, y)] += 1

                    if len(atom.arguments[1].arguments) == 2:
                        tile_name, rot = atom.arguments[1].arguments
                        
                        tile = plt.imread(FILE_PATH+tile_name.name+".png")
                        tile = np.rot90(tile, rot.number)
                        tile[:, :, 3] = 0.4
                        grid[y*SCALE:(y+1)*SCALE, x*SCALE:(x+1)*SCALE, :] += tile
                    elif len(atom.arguments[1].arguments) == 4:
                        r, g, b, a = atom.arguments[1].arguments
                        r = r.number/255
                        g = g.number/255
                        b = b.number/255
                        a = a.number/255
                        grid[y*SCALE:(y+1)*SCALE, x*SCALE:(x+1)*SCALE, :] += [r, g, b, a]


        if self.DEBUG:
            for (x, y), c in counts.items():
                grid[y*SCALE:(y+1)*SCALE, x*SCALE:(x+1)*SCALE, :] /= c       

            for (x, y), p in lowest_entropy:
                x = x.number-1
                y = y.number-1
                grid[y*SCALE:(y+1)*SCALE, x*SCALE:(x+1)*SCALE, 2] = 0.8
                grid[y*SCALE:(y+1)*SCALE, x*SCALE:(x+1)*SCALE, 3] = 0.5

            plt.imsave(f"process/img{self._t}.png", grid)

        if len(lowest_entropy) == 0: return

        ((x, y), p) = random.choices(population=lowest_entropy, weights=p_weights, k=1)[0]
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

        for i in range(0, self.width*self.height):

            self._t = i
            
            res = prg.solve(on_model=self.analyse_model)
            if not res.satisfiable: break
            
            print("step", i, f"({self._x}, {self._y})", self._p)

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
        
        if len(atom.arguments[1].arguments) == 2:
            # tile pattern (tile, rot)
            tile_name, rot = atom.arguments[1].arguments
            
            tile = plt.imread(folder_path+tile_name.name+".png")
            tile = np.rot90(tile, rot.number)

            grid[y*scale:(y+1)*scale, x*scale:(x+1)*scale, :] = tile
        elif len(atom.arguments[1].arguments) == 4:
            # pixel pattern (R, G, B, A)
            r, g, b, a = atom.arguments[1].arguments
            r = r.number/255
            g = g.number/255
            b = b.number/255
            a = a.number/255
            grid[y*scale:(y+1)*scale, x*scale:(x+1)*scale, :] = [r, g, b, a]

clingo_args = ["0", "--outf=3"]
# clingo_args = ["0", "--outf=3"]

with Profile() as profile:
    clingo_main(WFC(16, 16), sys.argv[1:] + clingo_args)
    (
        Stats(profile)
        .strip_dirs()
        .sort_stats("tottime")
        .print_stats(10)
    )

