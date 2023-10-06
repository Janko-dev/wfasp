import sys
from typing import Sequence
from clingo.application import Application, clingo_main
from clingo.control import Control
from clingo.symbol import Number, Function
from clingo.solving import Model

import random
import math

class WFC(Application):
    program_name = "WaveFunctionCollapse"
    version = "1.0"

    def __init__(self, height, width):
        self.width = width
        self.height = height
        self._r = 0
        self._c = 0
        self._s = ""
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

        (r, c, s) = random.choice(least_entropy)
        self._r = r
        self._c = c
        self._s = s
    
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

            print(self._r, self._c, self._s, i)

            prg.assign_external(
                Function("assigned", [
                    Number(self._r), Number(self._c),
                    Function(self._s), Number(i)
                ]), True)
        
        prg.solve()
            

clingo_main(WFC(2, 2), sys.argv[1:] + ["0"])

