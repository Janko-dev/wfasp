import json

class Rule:
    def __init__(self, base, neighbour, dir):
        self.base = base
        self.neighbour = neighbour
        self.dir = dir
    
    def __repr__(self) -> str:
        return f"rule({self.base}, {self.dir}, {self.neighbour})."
    
    def __hash__(self):
        return hash(self.__repr__())
    
    def __eq__(self, other):
        return (isinstance(other, Rule) and
                (self.base == other.base) and 
                (self.neighbour == other.neighbour) and 
                (self.dir == other.dir))

file_name = "input.json"
f = open(file_name)
data = json.load(f)

rules = set()
states = set()

grid = data["pattern"]
height = len(data["pattern"])
width = len(data["pattern"][0])


for i in range(len(grid)):
    for j in range(len(grid[i])):

        states.add(grid[i][j])

        if i - 1 >= 0:
            rules.add(Rule(grid[i][j], grid[i-1][j], "up"))
        if i + 1 < height:
            rules.add(Rule(grid[i][j], grid[i+1][j], "down"))
        if j - 1 >= 0:
            rules.add(Rule(grid[i][j], grid[i][j-1], "left"))
        if j + 1 < width:
            rules.add(Rule(grid[i][j], grid[i][j+1], "right"))
        

f = open(f"{data['file_name']}.lp", "w")


output = "\n".join(map(lambda rule: rule.__repr__(), rules))
output += "\n\n" + "\n".join([f"state({s})." for s in states])
print(output)

f.write(output)
f.close()