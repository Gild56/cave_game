import numpy as np


size = 16

x = np.linspace(0, 2 * np.pi, size)
z = np.linspace(0, 2 * np.pi, size)
X, Z = np.meshgrid(x, z)

heights = 11 + (np.sin(X) + np.cos(Z)) / 2 * 2

noise = np.random.uniform(-1, 1, size=(size, size))
heights += noise

heights = np.rint(heights).astype(int)

output_file = "start_world.txt"

with open(output_file, 'w') as f:
    for row in heights:
        f.write(' '.join(map(str, row)) + '\n')

output_file
