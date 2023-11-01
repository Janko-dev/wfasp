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

class Eval(Application):
    program_name = "Evaluation Wave Function Collapse (WFC)"
    version = "1.0"

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._x = 0
        self._y = 0
        self._p = None
        self._t = 0

    def analyse_model(self, model: Model):

        lowest_entropy = []
        p_weights = []
        for atom in model.symbols(atoms=True):

            if atom.match("lowest_entropy", 3):
                lowest_entropy.append((atom.arguments[0].arguments, atom.arguments[1].arguments))
                p_weights.append(atom.arguments[2].number)

        if len(lowest_entropy) == 0: return

        ((x, y), p) = random.choices(population=lowest_entropy, weights=p_weights, k=1)[0]
        self._x = x.number
        self._y = y.number
        self._p = p
    
    def eval_wfc(self, prg: Control):
        prev_cell = (-1, -1)
        global_restart = False
        total_runtime = 0

        for i in range(0, self.width*self.height):

            self._t = i
            res = prg.solve(on_model=self.analyse_model)
            total_runtime += prg.statistics["summary"]["times"]["solve"]
            
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
            exit(-1)
        return total_runtime

    def main(self, prg: Control, files: Sequence[str]):

        for file in files:
            prg.load(file)
        
        prg.ground([("rules", [])])

        prg.ground([("base", [
            Number(self.height), 
            Number(self.width)
        ])])

        # heuristics = ["berkmin,0", "vmtf,8", "vsids,95", "unit", "none"]
        heuristics = ["unit"]
        
        for heu in heuristics:
            prg.configuration.solver.heuristic = heu
            prg.configuration.solver.lookahead = "atom,1" if heu == "unit" else "no" 
            # prg.configuration.solver.lookahead = "no" 

            # print(prg.configuration.keys)
            # print(prg.configuration.solver.keys)
            # print(prg.configuration.solver.lookahead)
            # continue
            runtime = []
            choices = []
            for _ in range(10):
                for ext in prg.symbolic_atoms.by_signature("force", 3):
                    if ext.is_external: prg.assign_external(ext.symbol, False)
                solving_time = self.eval_wfc(prg)
                print(solving_time)
                runtime.append(solving_time)
                choices.append(prg.statistics["solving"]["solvers"]["choices"])
            # print(prg.statistics.keys())
            # print(prg.statistics["solving"])
            print(heu)
            print("runtime mean+std: ", np.mean(runtime), np.std(runtime))
            print("choices mean+std: ", np.mean(choices), np.std(choices))

        print("#vars", prg.statistics["problem"]["generator"]["vars"])
        print("#cons", prg.statistics["problem"]["generator"]["constraints"])


clingo_args = ["0", "--outf=3", "--stats"]#, "--lookahead=atom,5"]
SCALE = 128
ENCODING = "wfc_multishot.lp"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Wave Function Collapse')
    parser.add_argument('rules', type=str, help='path to rules logic program')
    parser.add_argument('-dim', type=int, nargs=2, help='width and height of output tiles')
    
    args = parser.parse_args()
    # print(args.rules)
    # # print(args.tile)
    # print(args.tileset_folder)
    # print(args.dim)
    # print(args.n)
    
    clingo_main(Eval(args.dim[0], args.dim[1]), [ENCODING, args.rules] + clingo_args)