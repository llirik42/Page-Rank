import random

from ranking import calculate_ranks, Pair

random.seed(1)
edges = []

for i in range(10):
    i1 = random.randint(1, 10)
    i2 = random.randint(1, 10)

    if i1 != i2:
        edges.append(Pair(i1, i2))

result = calculate_ranks(pairs=edges, precision=5, damping_factor=1)
print(result)
