import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

g = nx.DiGraph()

random.seed(0)

vertices_count = 20
edges_count = vertices_count * vertices_count // 2


for i in range(vertices_count):
    g.add_node(i)

for i in range(edges_count):
    v1 = random.randint(0, vertices_count - 1)
    v2 = random.randint(0, vertices_count - 1)

    if v1 != v2:
        g.add_edge(v1, v2)

nx.draw_networkx(g)
plt.show()

precision = 5
number_of_nodes: int = g.number_of_nodes()
fill_value: float = 1 / number_of_nodes
ranks: np.ndarray = np.full(shape=(number_of_nodes, 1), fill_value=fill_value)
matrix = np.zeros((number_of_nodes, number_of_nodes))

for e in g.edges:
    matrix[e[1]][e[0]] = 1

sums: list[int] = [sum(c) for c in matrix.transpose()]

for i in range(number_of_nodes):
    for j in range(number_of_nodes):
        current_sum: int = sums[j]
        matrix[i][j] = fill_value if current_sum == 0 else matrix[i][j] / current_sum

d = 1

b = np.full(shape=(number_of_nodes, 1), fill_value=1-d)

iterations = 0
epsilon = 10 ** (-precision)
while True:
    new_ranks = b + d * matrix.dot(ranks)
    diff = np.linalg.norm(ranks - new_ranks)
    ranks = new_ranks

    iterations += 1

    if diff < epsilon:
        break

print(iterations)
result = {i: ranks[i][0] for i in range(number_of_nodes)}
sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)

print(sorted_result)
