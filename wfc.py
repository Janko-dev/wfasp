import sys
from typing import Sequence
from clingo.application import Application, clingo_main
from clingo.control import Control
from clingo.symbol import Number, Function, String
from clingo.solving import Model

import random
import math

class WFC(Application):
    program_name = "WaveFunctionCollapse"
    version = "1.0"

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.entropy = {}
        self.collapsed = {}

    def calc_entropy(self, model: Model):
        
        for atom in model.symbols(atoms=True):
            if atom.match("superpos", 3):
                r = atom.arguments[0].number
                c = atom.arguments[1].number
                
                if (r, c) in self.collapsed: continue

                if (r, c) not in self.entropy: 
                    self.entropy[(r, c)] = {atom.arguments[2].name}
                else:
                    self.entropy[(r, c)].add(atom.arguments[2].name)
    
    def register_collapsed(self, model: Model):
        
        for atom in model.symbols(atoms=True):
            if atom.match("collapsed", 3):
                r = atom.arguments[0].number
                c = atom.arguments[1].number
                
                self.collapsed[(r, c)] = atom.arguments[2].name


    def main(self, ctl: Control, files: Sequence[str]):

        for file in files:
            ctl.load(file)
        
        ctl.ground([("base", [Number(self.width), Number(self.height)])])

        ctl.assign_external(
                Function("collapsed", [
                    Number(1), Number(1),
                    Function("a")
                ]), True)
        
        ctl.assign_external(
                Function("collapsed", [
                    Number(3), Number(3),
                    Function("b")
                ]), True)
        
        ctl.assign_external(
                Function("collapsed", [
                    Number(4), Number(2),
                    Function("b")
                ]), True)

        # final_model = None
        iteration = 1
        while True:
            
            # print("Iteration", iteration)
            # solve super positions that adhere to collapsed cells
            with ctl.solve(yield_=True) as handle:
                self.entropy = {}
                for model in handle:
                    self.register_collapsed(model)
                    self.calc_entropy(model)

                # print(self.entropy)
            if len(self.entropy) == 0: 
                # for model in handle:
                #     print(model)
                # final_model = handle
                # print(ctl.statistics)
                break


            # pick random position and collapse it
            minimum = len(min(self.entropy.values()))
            
            state_choices = [
                (k, v) 
                for k, v in self.entropy.items() 
                if len(v) == minimum
            ]
            
            (r, c), state = random.choice(state_choices)
            # print(state_choices)
            # print(r, c, state)

            ctl.assign_external(
                Function("collapsed", [
                    Number(r), Number(c),
                    Function(random.choice(tuple(state)))
                ]), True)
            
            iteration += 1

        # print(final_model)
        # print(ctl.statistics)
            

clingo_main(WFC(4, 4), sys.argv[1:] + ["0", "--outf=2"])