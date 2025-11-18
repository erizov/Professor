import os
import pytest

from .conftest import algorithm_file_path, import_module_from_path, find_callable

GRAPH_ALGOS = {
    "bfs": [
        "semester_01",
        "lecture_09_graph_algorithms",
        "bfs",
        "bfs.py",
    ],
    "dfs": [
        "semester_01",
        "lecture_09_graph_algorithms",
        "dfs",
        "dfs.py",
    ],
    "dijkstra": [
        "semester_01",
        "lecture_09_graph_algorithms",
        "dijkstra",
        "dijkstra.py",
    ],
}


def small_graph():
    # Simple undirected/unweighted graph for BFS/DFS
    return {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }


def weighted_graph():
    return {
        'A': {'B': 1, 'C': 4},
        'B': {'C': 2, 'D': 5},
        'C': {'D': 1},
        'D': {}
    }


@pytest.mark.parametrize("algo_name, path_parts", GRAPH_ALGOS.items())
def test_graph_algorithms(algo_name, path_parts):
    path = algorithm_file_path(*path_parts)
    if not os.path.exists(path):
        pytest.skip(f"Algorithm file not found: {path}")

    module = import_module_from_path(path)
    fn = find_callable(module, [algo_name])
    if fn is None:
        pytest.skip(f"No callable function {algo_name} found in {path}")

    if algo_name in ("bfs", "dfs"):
        g = small_graph()
        order = fn(g, 'A')
        assert 'A' in order
        assert set(order) <= set(g.keys())
    elif algo_name == "dijkstra":
        g = weighted_graph()
        dist = fn(g, 'A')
        assert dist['A'] == 0
        assert dist['D'] == 4  # A->B (1), B->C (2), C->D (1) total 4
