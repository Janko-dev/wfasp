from pstats import Stats
import sys
from typing import Sequence
from clingo import StatisticsMap, Symbol
from clingo.application import Application, clingo_main
from clingo.control import Control
from clingo.symbol import Number, Function
from clingo.solving import Model
from cProfile import Profile

import numpy as np
import matplotlib.pyplot as plt

class WFCEval(Application):
    program_name = "Evaluation of Tiled Wave Function Collapse (TWFC)"
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

        # heuristics = ["berkmin,0", "vmtf,8", "vsids,95", "domain", "unit", "none"]
        heuristics = ["berkmin,0", "vmtf,8", "vsids,95", "domain", "none"]

        for heu in heuristics:
            prg.configuration.solver.heuristic = heu
            runtime = []
            choices = []
            for _ in range(10):
                prg.solve()
                runtime.append(prg.statistics["summary"]["times"]["solve"])
                choices.append(prg.statistics["solving"]["solvers"]["choices"])
            # print(prg.statistics.keys())
            # print(prg.statistics["solving"])
            print(heu)
            print("runtime mean+std: ", np.mean(runtime), np.std(runtime))
            print("choices mean+std: ", np.mean(choices), np.std(choices))

        print("#vars", prg.statistics["problem"]["generator"]["vars"])
        print("#cons", prg.statistics["problem"]["generator"]["constraints"])


# clingo_args = ["0", "--outf=3"]
# clingo_args = ["1", "--stats"]
clingo_args = ["1", "--stats", "--outf=3"]

clingo_main(WFCEval(16, 16), sys.argv[1:] + clingo_args)

# heuristics = ["Berkmin", "Vmtf", "Vsids", "Domain", "Unit", "None"]
