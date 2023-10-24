from pstats import Stats
import sys
from typing import Sequence
from clingo import Symbol
from clingo.application import Application, clingo_main
from clingo.control import Control
from clingo.symbol import Number, Function
from clingo.solving import Model
from cProfile import Profile

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

    def main(self, prg: Control, files: Sequence[str]):

        for file in files:
            prg.load(file)

        prg.ground([("rules", [])])

        prg.ground([("base", [
            Number(self.height), 
            Number(self.width)
        ])])

        prg.ground([("input", [])])

        with prg.solve(yield_=True) as models:
            for (i, model) in enumerate(models):
                self.visualize(model, i)

    def visualize(self, model: Model, i):
        
        grid = np.zeros((self.height*SCALE, self.width*SCALE, 4))
        for atom in model.symbols(shown=True):
            write_tile_to_buf(atom, grid, FILE_PATH, SCALE)

        plt.imsave(f"process/img{i}.png", grid)

def write_tile_to_buf(atom: Symbol, grid: np.ndarray, folder_path: str, scale: int):
    if atom.match("assigned", 2): 
        (x, y) = atom.arguments[0].arguments
        x = x.number - 1
        y = y.number - 1
        tile_name, rot = atom.arguments[1].arguments
        
        tile = plt.imread(folder_path+tile_name.name+".png")
        tile = np.rot90(tile, rot.number)

        grid[y*scale:(y+1)*scale, x*scale:(x+1)*scale, :] = tile

# clingo_args = ["0", "--outf=3"]
clingo_args = ["1", "--outf=3"]

with Profile() as profile:
    clingo_main(WFC(4, 4), sys.argv[1:] + clingo_args)
    (
        Stats(profile)
        .strip_dirs()
        .sort_stats("tottime")
        .print_stats(10)
    )
