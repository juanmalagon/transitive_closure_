from collections import defaultdict
from typing import List, Tuple, Any, Iterable
from scipy.sparse import lil_matrix
import itertools


class Graph:
    """A directed graph class for computing transitive closure using DFS.

    Attributes:
        V (int): Number of vertices in the graph
        graph (defaultdict): Adjacency list representation of the graph
        tc (lil_matrix): Transitive closure matrix in sparse format
    """

    def __init__(self, vertices: int) -> None:
        """Initialize graph with given number of vertices.

        Args:
            vertices: Number of vertices in the graph
        """
        self.V = vertices
        self.graph: defaultdict[int, List[int]] = defaultdict(list)
        self.tc = lil_matrix((self.V, self.V), dtype=int)

    def addEdge(self, u: int, v: int) -> None:
        """Add a directed edge from vertex u to vertex v.

        Args:
            u: Source vertex index
            v: Target vertex index
        """
        self.graph[u].append(v)

    def _DFSUtil(self, s: int, v: int) -> None:
        """Recursive DFS helper for transitive closure computation.

        Args:
            s: Source vertex index for closure computation
            v: Current vertex index being visited
        """
        self.tc[s, v] = 1
        for neighbor in self.graph[v]:
            if self.tc[s, neighbor] == 0:
                self._DFSUtil(s, neighbor)

    def transitiveClosure(self) -> None:
        """Compute transitive closure matrix using DFS for all vertices."""
        for i in range(self.V):
            print(f"Transitive closure of {i} out of {self.V} completed")
            self._DFSUtil(i, i)


def dfs_transitive_closure(
    iterable: Iterable[Any], tuples: List[Tuple[Any, Any]]
) -> List[Tuple[Any, Any]]:
    """Compute transitive closure of a relation using DFS.

    Args:
        iterable: Collection of unique elements representing all nodes
        tuples: List of tuples representing edges in the relation

    Returns:
        List of tuples representing the transitive closure of the input relation

    Example:
        >>> dfs_transitive_closure(['a', 'b'], [('a', 'b')])
        [('a', 'a'), ('a', 'b'), ('b', 'b')]
    """
    elements = list(iterable)
    enumeration = list(enumerate(elements))
    num_to_idi = dict(enumeration)
    idi_to_num = {element: idx for idx, element in enumeration}

    tuples_num = [(idi_to_num[u], idi_to_num[v]) for u, v in tuples]

    graph = Graph(len(elements))
    for u, v in tuples_num:
        graph.addEdge(u, v)

    graph.transitiveClosure()

    tuples_final = [
        (m, n)
        for m in range(len(elements))
        for n in range(len(elements))
        if graph.tc[m, n] == 1
    ]

    return [(num_to_idi[u], num_to_idi[v]) for u, v in tuples_final]


def make_equivalence_classes(
    iterable: Iterable[Any], tuples: List[Tuple[Any, Any]]
) -> List[List[Any]]:
    """Partition elements into equivalence classes based on relation.

    Args:
        iterable: Collection of unique elements to be partitioned
        tuples: List of tuples representing the equivalence relation

    Returns:
        List of equivalence classes (lists of equivalent elements)

    Example:
        >>> make_equivalence_classes([1,2,3], [(1,2), (2,1)])
        [[1, 2], [3]]
    """
    elements = list(iterable)
    enumeration = list(enumerate(elements))
    num_to_idi = dict(enumeration)
    idi_to_num = {element: idx for idx, element in enumeration}

    tuples_num = [(idi_to_num[u], idi_to_num[v]) for u, v in tuples]

    graph = Graph(len(elements))
    for u, v in tuples_num:
        graph.addEdge(u, v)

    graph.transitiveClosure()

    # Get non-zero elements from transitive closure matrix
    nonzero_indices = zip(graph.tc.nonzero()[0], graph.tc.nonzero()[1])

    # Group by source vertex to form equivalence classes
    classes: List[List[Any]] = []
    for source, group in itertools.groupby(sorted(nonzero_indices), key=lambda x: x[0]):
        equivalence_class = [target for _, target in group]
        equivalence_class_idi = sorted([num_to_idi[item] for item in equivalence_class])
        classes.append(equivalence_class_idi)
        print(f"Equivalence class of {source} out of {len(elements)} detected")

    # Remove duplicates and return
    return [list(x) for x in {tuple(x) for x in classes}]
