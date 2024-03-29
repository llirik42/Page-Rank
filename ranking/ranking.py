import typing
from dataclasses import dataclass
import numpy as np

from .pair import Pair
from .ranked_object import RankedObject


@dataclass
class Edge:
    src: int
    dst: int


float_array = np.ndarray[typing.Any, np.dtype[np.float64]]


def calculate_ranks(
        pairs: list[Pair],
        precision: int = 5,
        damping_factor: float = 1) -> list[RankedObject]:
    unique_objects: list[object] = _find_unique_objects_in_pairs(pairs)
    unique_objects_count: int = len(unique_objects)

    if unique_objects_count == 0:
        return []

    enumerated_objects: dict[object, int] = _enumerate_objects(unique_objects)

    graph_edges: list[Edge] = _enumerated_objects_to_edges(
        pairs=pairs,
        enumerated_objects=enumerated_objects
    )

    graph_ranks: list[float] = calculate_graph_ranks(
        number_of_vertices=unique_objects_count,
        edges=graph_edges,
        precision=precision,
        damping_factor=damping_factor
    )

    unsorted_result: list[RankedObject] = [(
        RankedObject(obj=unique_objects[i], rank=graph_ranks[i])
    ) for i in range(unique_objects_count)]

    return sorted(unsorted_result, key=lambda x: x.rank, reverse=True)


def calculate_graph_ranks(
        number_of_vertices: int,
        edges: list[Edge],
        precision: int,
        damping_factor: float) -> list[float]:
    matrix: float_array = _calculate_matrix(
        number_of_vertices=number_of_vertices,
        edges=edges
    )

    damping_vector: float_array = _get_damping_vector(
        number_of_vertices=number_of_vertices,
        damping_factor=damping_factor
    )

    epsilon: float = 0.1 ** precision

    ranks: float_array = _iterate(
        start_ranks=_get_start_ranks(number_of_vertices),
        epsilon=epsilon,
        matrix=matrix,
        damping_vector=damping_vector,
        damping_factor=damping_factor
    )

    return [r[0] for r in ranks]


def _find_unique_objects_in_pairs(pairs: list[Pair]) -> list[object]:
    unique_objects_set: set[object] = set()

    for pair in pairs:
        unique_objects_set.add(pair.src)
        unique_objects_set.add(pair.dst)

    return list(unique_objects_set)


def _get_start_ranks(number_of_vertices: int) -> float_array:
    return np.full(
        shape=(number_of_vertices, 1),
        fill_value=1 / number_of_vertices
    )


def _get_damping_vector(number_of_vertices: int, damping_factor: float) -> float_array:
    return np.full(shape=(number_of_vertices, 1), fill_value=1 - damping_factor)


def _calculate_matrix(number_of_vertices: int, edges: list[Edge]) -> float_array:
    matrix: float_array = np.zeros((number_of_vertices, number_of_vertices))
    fill_value: float = 1 / number_of_vertices

    for e in edges:
        matrix[e.dst][e.src] = 1

    sums: list[int] = [sum(c) for c in matrix.transpose()]

    for i in range(number_of_vertices):
        for j in range(number_of_vertices):
            current_sum: int = sums[j]
            matrix[i][j] = fill_value if current_sum == 0 else matrix[i][j] / current_sum

    return matrix


def _iterate(start_ranks: float_array,
             epsilon: float,
             matrix: float_array,
             damping_vector: float_array,
             damping_factor: float) -> float_array:
    ranks: float_array = start_ranks

    while True:
        new_ranks: float_array = damping_vector + damping_factor * matrix.dot(ranks)
        diff: float = float(np.linalg.norm(ranks - new_ranks))
        ranks = new_ranks

        if diff < epsilon:
            break

    return ranks


def _enumerate_objects(objects: list[object]) -> dict[object, int]:
    result: dict[object, int] = dict()

    for unique in objects:
        result[unique] = len(result)

    return result


def _enumerated_objects_to_edges(
        pairs: list[Pair],
        enumerated_objects: dict[object, int]) -> list[Edge]:
    return [Edge(
        enumerated_objects[pair.src],
        enumerated_objects[pair.dst]
    ) for pair in pairs]