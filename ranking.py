import numpy as np


def calculate_ranks(
        pairs: list[tuple[object, object]],
        precision: int = 5,
        d: float = 1) -> list[tuple[float, object]]:
    unique_objects: list[object] = _find_unique_objects_in_tuples(pairs)
    unique_objects_count: int = len(unique_objects)

    if unique_objects_count == 0:
        return []

    enumerated_objects: dict[object, int] = _enumerate_objects(unique_objects)

    edges: list[tuple[int, int]] = _enumerated_objects_to_edges(
        object_pairs=pairs,
        enumerated_objects=enumerated_objects
    )

    graph_ranks: list[float] = calculate_graph_ranks(
        number_of_vertices=unique_objects_count,
        edges=edges,
        precision=precision,
        d=d
    )

    unsorted_result: list[tuple[float, object]] = [(
        graph_ranks[i],
        unique_objects[i]
    ) for i in range(unique_objects_count)]

    return sorted(unsorted_result, key=lambda x: x[0], reverse=True)


def calculate_graph_ranks(
        number_of_vertices: int,
        edges: list[tuple[int, int]],
        precision: int,
        d: float) -> list[float]:
    matrix: np.ndarray = _calculate_matrix(
        number_of_vertices=number_of_vertices,
        edges=edges
    )

    b: np.ndarray = _get_b(
        number_of_vertices=number_of_vertices,
        d=d
    )

    epsilon: float = 0.1 ** precision

    ranks: np.ndarray = _iterate(
        start_ranks=_get_start_ranks(number_of_vertices),
        epsilon=epsilon,
        matrix=matrix,
        b=b,
        d=d
    )

    return [r[0] for r in ranks]


def _find_unique_objects_in_tuples(tuples: list[tuple[object, object]]) -> list[object]:
    unique_objects_set: set[object] = set()

    for pair in tuples:
        unique_objects_set.add(pair[0])
        unique_objects_set.add(pair[1])

    return list(unique_objects_set)


def _get_start_ranks(number_of_vertices: int) -> np.ndarray:
    return np.full(
        shape=(number_of_vertices, 1),
        fill_value=1 / number_of_vertices
    )


def _get_b(number_of_vertices: int, d: float) -> np.ndarray:
    return np.full(shape=(number_of_vertices, 1), fill_value=1 - d)


def _calculate_matrix(number_of_vertices: int, edges: list[tuple[int, int]]) -> np.ndarray:
    matrix: np.ndarray = np.zeros((number_of_vertices, number_of_vertices))
    fill_value: float = 1 / number_of_vertices

    for e in edges:
        matrix[e[1]][e[0]] = 1

    sums: list[int] = [sum(c) for c in matrix.transpose()]

    for i in range(number_of_vertices):
        for j in range(number_of_vertices):
            current_sum: int = sums[j]
            matrix[i][j] = fill_value if current_sum == 0 else matrix[i][j] / current_sum

    return matrix


def _iterate(start_ranks: np.ndarray, epsilon: float, matrix: np.ndarray, b: np.ndarray, d: float) -> np.ndarray:
    ranks: np.ndarray = start_ranks

    while True:
        new_ranks: np.ndarray = b + d * matrix.dot(ranks)
        diff: float = np.linalg.norm(ranks - new_ranks)
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
        object_pairs: list[tuple[object, object]],
        enumerated_objects: dict[object, int]) -> list[tuple[int, int]]:
    return [(enumerated_objects[pair[0]], enumerated_objects[pair[1]]) for pair in object_pairs]
