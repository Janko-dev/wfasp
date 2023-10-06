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
        self.entropy = {}
        self.assigned = {}

    def calc_entropy(self, model: Model):
        
        for atom in model.symbols(atoms=True):
            if atom.match("superpos", 3):
                r = atom.arguments[0].number
                c = atom.arguments[1].number
                
                if (r, c) in self.assigned: continue

                if (r, c) not in self.entropy: 
                    self.entropy[(r, c)] = {atom.arguments[2].name}
                else:
                    self.entropy[(r, c)].add(atom.arguments[2].name)
    
    def register_assigned(self, model: Model):
        
        for atom in model.symbols(atoms=True):
            if atom.match("assigned", 4):
                r = atom.arguments[0].number
                c = atom.arguments[1].number
                
                self.assigned[(r, c)] = atom.arguments[2].name

    def _on_model(self, model):

        self.register_assigned(model)
        self.calc_entropy(model)
    
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
                Number(2), Number(4),
                Function("c"), Number(0)
            ]), True)
        
        # iteration
        for i in range(1, iters):

            prg.ground([("step", [Number(i)])])
            
            self.entropy = {}

            prg.solve(on_model=self._on_model)

            if len(self.entropy) == 0:
                break

            minimum = len(min(self.entropy.values()))
            
            state_choices = [
                (k, v) 
                for k, v in self.entropy.items() 
                if len(v) == minimum
            ]
            
            (r, c), state = random.choice(state_choices)
            print(state_choices)
            return
            # print(r, c, state)

            prg.assign_external(
                Function("assigned", [
                    Number(r), Number(c),
                    Function(random.choice(tuple(state)))
                ]), True)
        
        prg.solve(on_model=self.print)
    
    def print(self, model):
        print(model)

# args = ["0", "--outf=3"]
args = ["0"]

clingo_main(WFC(2, 4), sys.argv[1:] + args)

