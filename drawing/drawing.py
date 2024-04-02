import networkx as nx
from matplotlib import pyplot as plt

from dto import Pair


def draw_graph(pairs: list[Pair]):
    g = nx.DiGraph()

    for pair in pairs:
        g.add_edge(pair.src, pair.dst, weight=pair.weight)

    pos = nx.spring_layout(g)
    nx.draw(g, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=10, arrows=True)

    plt.show()
