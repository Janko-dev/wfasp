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

    def __init__(self):
        self.n = 3
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
        
        # print(ctl._rep)
        # ctl = Control("0")

        for file in files:
            ctl.load(file)
        
        ctl.ground([("base", [Number(self.n)])])
        ctl.ground([("step", [])])

        ctl.assign_external(
                Function("collapsed", [
                    Number(1), Number(1),
                    Function("a")
                ]), True)

        for i in range(10):


            # calculate super positions based on collapsed cells
            with ctl.solve(yield_=True) as handle:
                self.entropy = {}
                for model in handle:
                    # print(i+1, "Answer set: ", model)
                    self.register_collapsed(model)
                    self.calc_entropy(model)
                print(self.entropy)
                if len(self.entropy) == 0: 
                    for model in handle:
                        print(model)
                    break


            # # pick random position and collapse it
            minimum = len(min(self.entropy.values()))
            # lowest_entropy = math.inf
            
            # for super_state in sorted_super_states:
            #     len_set = len(super_state)
            #     if len_set > 1 and len_set < lowest_entropy:
            #         lowest_entropy = len_set
            
            state_choices = [(k, v) for k, v in self.entropy.items() if len(v) == minimum]
            
            print(state_choices)
            (r, c), state = random.choice(state_choices)
            print(r, c, state)

            ctl.assign_external(
                Function("collapsed", [
                    Number(r), Number(c),
                    Function(random.choice(tuple(state)))
                ]), True)

            


clingo_main(WFC(), sys.argv[1:] + ["0"])