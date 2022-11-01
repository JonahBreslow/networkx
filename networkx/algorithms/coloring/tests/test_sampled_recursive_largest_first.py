"""sampled recursive largest first test suite.

"""
import pytest

import networkx as nx

is_coloring = nx.algorithms.coloring.equitable_coloring.is_coloring


# ############################  Graph Generation ############################


def empty_graph():
    return nx.Graph()


def one_node_graph():
    graph = nx.Graph()
    graph.add_nodes_from([1])
    return graph


def two_node_graph():
    graph = nx.Graph()
    graph.add_nodes_from([1, 2])
    graph.add_edges_from([(1, 2)])
    return graph


def three_node_clique():
    graph = nx.Graph()
    graph.add_nodes_from([1, 2, 3])
    graph.add_edges_from([(1, 2), (1, 3), (2, 3)])
    return graph


def disconnected():
    graph = nx.Graph()
    graph.add_edges_from([(1, 2), (2, 3), (4, 5), (5, 6)])
    return graph


# --------------------------------------------------------------------------
# Basic tests for all strategies
# For each basic graph function, specify the number of expected colors.
BASIC_TEST_CASES = {
    empty_graph: 0,
    one_node_graph: 1,
    two_node_graph: 2,
    disconnected: 2,
    three_node_clique: 3,
}


# ############################  tests ############################


@pytest.mark.parametrize(
    "graph_func, n_nodes", [(k, v) for k, v in BASIC_TEST_CASES.items()]
)
@pytest.mark.parametrize("n_searches", [10, 100, 1_000, 10_000])
def test_basic_case(graph_func, n_nodes, n_searches):
    graph = graph_func()
    coloring = nx.coloring.sampled_rlf(graph, n_searches=n_searches)
    print(coloring)
    assert verify_length(coloring, n_nodes)
    assert verify_coloring(graph, coloring)


def test_bad_inputs():
    graph = one_node_graph()
    pytest.raises(
        nx.NetworkXError,
        nx.coloring.sampled_rlf,
        graph,
        n_searches="invalid search",
    )


#  ############################  Utility functions ############################
def verify_coloring(graph, coloring):
    for node in graph.nodes():
        if node not in coloring:
            return False

        color = coloring[node]
        for neighbor in graph.neighbors(node):
            if coloring[neighbor] == color:
                return False

    return True


def verify_length(coloring, expected):
    coloring = dict_to_sets(coloring)
    return len(coloring) == expected


def dict_to_sets(colors):
    if len(colors) == 0:
        return []

    k = max(colors.values()) + 1
    sets = [set() for _ in range(k)]

    for (node, color) in colors.items():
        sets[color].add(node)

    return sets
