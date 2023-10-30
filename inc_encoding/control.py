from __future__ import annotations
from typing import Sequence
from clingo import Symbol
from clingo.application import Application, clingo_main
from clingo.control import Control
from clingo.symbol import Number, Function
from clingo.solving import Model
from cProfile import Profile
from pstats import SortKey, Stats

import random
import argparse

import numpy as np
import matplotlib.pyplot as plt
import cv2

class WFC(Application):
    program_name = "Wave Function Collapse (WFC)"
    version = "1.0"

    def __init__(self, width: int, height: int, tileset_path: str, scale: int, n: int = 1):
        self.padx = width % n
        self.pady = height % n
        # print(self.padx, self.pady)
        self.width = width
        self.height = height
        self._x = 0
        self._y = 0
        self._p = None
        self._t = 0
        # self.DEBUG = False
        self.DEBUG = True
        self.tileset_path = tileset_path
        self.scale = scale
        # self.n = n

    def analyse_model(self, model: Model):

        if self.DEBUG:
            grid = np.zeros(((self.height+self.pady)*self.scale, (self.width+self.padx)*self.scale, 4), dtype="uint8")
            counts = {}

        lowest_entropy = []
        p_weights = []
        for atom in model.symbols(atoms=True):

            if atom.match("lowest_entropy", 3):
                lowest_entropy.append((atom.arguments[0].arguments, atom.arguments[1].arguments))
                p_weights.append(atom.arguments[2].number)
            
            if self.DEBUG:
                if atom.match("assigned", 2):
                    self.write_assigned(atom, grid)

                # if atom.match("superpos", 2):
                #     self.write_superpos(atom, grid, counts)
                
        if self.DEBUG:
            # for (x, y), c in counts.items():
            #     temp = (grid[y*self.scale:(y+1)*self.scale, x*self.scale:(x+1)*self.scale, :] / c)
            #     grid[y*self.scale:(y+1)*self.scale, x*self.scale:(x+1)*self.scale, :] = temp.astype("uint8")
            
            for (x, y), p in lowest_entropy:
                x = x.number-1
                y = y.number-1
                grid[y*self.scale:(y+1)*self.scale, x*self.scale:(x+1)*self.scale, 2] = 180
                grid[y*self.scale:(y+1)*self.scale, x*self.scale:(x+1)*self.scale, 3] = 120
                    
            grid = grid[:-self.pady*self.scale or None, :-self.padx*self.scale or None, :].copy(order="C")
            plt.imsave(f"process/img{self._t}.png", grid)

        if len(lowest_entropy) == 0: return

        ((x, y), p) = random.choices(population=lowest_entropy, weights=p_weights, k=1)[0]
        self._x = x.number
        self._y = y.number
        self._p = p
    
    def solve_wfc(self, prg: Control):
        prev_cell = (-1, -1)
        global_restart = False

        for i in range(0, self.width*self.height):

            self._t = i
            
            res = prg.solve(on_model=self.analyse_model)
            
            print("Step", i, f"({self._x}, {self._y})", self._p)

            if not res.satisfiable or prev_cell == (self._x, self._y):
                global_restart = True
                break
            
            prev_cell = (self._x, self._y)

            prg.assign_external(Function("force", [
                Number(self._x), Number(self._y), 
                Function("", self._p)
            ]), True)
        
        if global_restart:
            print("\nEncountered unsatisfiable constraint, globally restarting solver\n")
            for ext in prg.symbolic_atoms.by_signature("force", 3):
                if ext.is_external: prg.assign_external(ext.symbol, False)
            self.solve_wfc(prg)
        else:
            self._t += 1
            prg.solve(on_model=self.analyse_model)

    def main(self, prg: Control, files: Sequence[str]):

        for file in files:
            prg.load(file)
        
        prg.ground([("rules", [])])

        prg.ground([("base", [
            Number(self.height), 
            Number(self.width)
        ])])

        prg.ground([("input", [])])
        
        self.solve_wfc(prg)

        prg.solve(on_model=self.visualize)

    def visualize(self, model: Model):
        
        grid = np.zeros(((self.height+self.pady)*self.scale, (self.width+self.padx)*self.scale, 4), dtype="uint8")

        for atom in model.symbols(atoms=True):
            if atom.match("assigned", 2):
                self.write_assigned(atom, grid)

        grid = grid[:-self.scale*self.pady or None, :-self.scale*self.padx or None, :].copy(order="C")
        plt.imsave("img.png", grid)


    def write_assigned(self, atom: Symbol, grid: np.ndarray):
        
        (x, y) = atom.arguments[0].arguments
        x = x.number - 1
        y = y.number - 1
        pattern = 0

        if len(atom.arguments[1].arguments) == 2 and self.tileset_path and atom.arguments[1].arguments[0].name != "":
            # tile pattern (tile, rot)
            tile_name, rot = atom.arguments[1].arguments
            tile = plt.imread(self.tileset_path+tile_name.name+".png")
            tile = np.rot90(tile, rot.number)
            pattern = (tile * 255).astype("uint8")
            
        elif len(atom.arguments[1].arguments) == 4:
            # pixel pattern (R, G, B, A)
            r, g, b, a = atom.arguments[1].arguments
            pattern = [r.number/255, g.number/255, b.number/255, a.number/255]
        else:
            # N X M region pattern ((p1, ..., pn), ..., (p1, ..., pn)) where p_i = (R, G, B, A)
            data = np.array([[[num.number for num in col.arguments] for col in row.arguments] for row in atom.arguments[1].arguments])
            data_resized = cv2.resize(data.astype("uint8"), dsize=(self.scale, self.scale), interpolation=cv2.INTER_NEAREST)
            pattern = data_resized

        grid[y*self.scale:(y+1)*self.scale, x*self.scale:(x+1)*self.scale, :] = pattern

    def write_superpos(self, atom: Symbol, grid: np.ndarray, counts: dict[tuple[int]]):
        
        (x, y) = atom.arguments[0].arguments
        x = x.number - 1
        y = y.number - 1

        if (x, y) not in counts: counts[(x, y)] = 1
        else: counts[(x, y)] += 1

        pattern = [0, 0, 0, 0]

        if len(atom.arguments[1].arguments) == 2 and self.tileset_path and atom.arguments[1].arguments[0].name != "":
            # tile pattern (tile, rot)
            tile_name, rot = atom.arguments[1].arguments
            tile = plt.imread(self.tileset_path+tile_name.name+".png")
            tile = np.rot90(tile, rot.number)
            pattern = (tile * 255).astype("uint8")

        elif len(atom.arguments[1].arguments) == 4:
            # pixel pattern (R, G, B, A)
            r, g, b, a = atom.arguments[1].arguments
            pattern = [r.number/255, g.number/255, b.number/255, a.number/255]
        else:
            # N X M region pattern ((p1, ..., pn), ..., (p1, ..., pn)) where p_i = (R, G, B, A)
            data = np.array([[[num.number for num in col.arguments] for col in row.arguments] for row in atom.arguments[1].arguments])
            data_resized = cv2.resize(data.astype("uint8"), dsize=(self.scale, self.scale), interpolation=cv2.INTER_NEAREST)
            pattern = data_resized

        grid[y*self.scale:(y+1)*self.scale, x*self.scale:(x+1)*self.scale, :] += pattern





clingo_args = ["0", "--outf=3"]
SCALE = 128
ENCODING = "wfc_multishot.lp"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Wave Function Collapse')
    parser.add_argument('rules', type=str, help='path to rules logic program')
    parser.add_argument('tileset_folder', type=str, nargs='?', help='path to folder with .png tileset.')
    parser.add_argument('-n', type=int, nargs='?', help='number of patterns in NxN square to consider')
    parser.add_argument('-dim', type=int, nargs=2, help='width and height of output image')
    
    args = parser.parse_args()
    # print(args.rules)
    # # print(args.tile)
    # print(args.tileset_folder)
    # print(args.dim)
    # print(args.n)
    
    with Profile() as profile:
        clingo_main(
            WFC(
                args.dim[0], 
                args.dim[1], 
                args.tileset_folder, 
                SCALE, 
                args.n if args.n else 1
            ), 
            [ENCODING, args.rules] + clingo_args)
        (
            Stats(profile)
            .strip_dirs()
            .sort_stats("tottime")
            .print_stats(10)
        )

