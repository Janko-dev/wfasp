import numpy as np
import matplotlib.pyplot as plt
import sys
import json

file_name = sys.argv[1]
f = open(file_name)

data = json.load(f)

print(data)

# # parse "grid(R, C, X)" as [R, C, X]
# data = [tuple(int(x) for x in el[5:-1].split(",")) for el in data]

# rows = max(data, key=lambda x: x[0])[0]
# cols = max(data, key=lambda x: x[1])[1]

# mat = [[0 for _ in range(cols)] for _ in range(rows)]

# for (r, c, x) in data:
#     mat[r-1][c-1] = x

# grid = np.array(mat)

# # print(grid)

# plt.imshow(grid)
# plt.show()