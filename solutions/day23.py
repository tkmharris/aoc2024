import re
from utils.solver import Solver
from utils.input import read_input
from collections import defaultdict, OrderedDict
from typing import TypeVar
from itertools import islice


T = TypeVar("T")


def triangles(graph: dict[T, list[T]]) -> list[set[T]]:
    """
    Return all 3-cliques (triangles) in a graph.
    Algorithm here taken from Arboricity and Subgraph Listing Algorithms
    (Chiba & Nishizeki, 1985).
    """
    ordered_graph = OrderedDict()
    for vertex in sorted(graph, key=lambda k: -len(graph[k])):
        ordered_graph[vertex] = graph[vertex]

    results = set()
    for vertex1, adjacent_vertices in ordered_graph.items():
        for vertex2 in adjacent_vertices:
            for vertex3 in graph[vertex2]:
                if vertex3 in adjacent_vertices:
                    results.add((vertex1, vertex2, vertex3))
        
    return list(map(set, {frozenset(result) for result in results}))


def maximal_cliques(graph: dict[T, list[T]]) -> list[set[T]]:
    """
    Return all maximal cliques in a graph.
    Uses the Bron-Kerbosch algorithm.
    """
    maximal_cliques: list[set[T]] = []
    vertices: set[T] = set(graph.keys())

    def bron_kerbosch(include: set[T], consider: set[T], exclude: set[T]):
        if not (consider or exclude):
            maximal_cliques.append(include)
        
        for vertex in list(consider):
            bron_kerbosch(
                include.union([vertex]), 
                consider.intersection(graph[vertex]), 
                exclude.intersection(graph[vertex])
            )
            consider.remove(vertex)
            exclude.add(vertex)    

    bron_kerbosch(set(), vertices, set())
    return maximal_cliques


class Day23(Solver):
    def setup(self, lines: list[str]) -> dict[str, set[str]]:
        graph = defaultdict(set)
        for line in lines:
            match = re.match(r'([a-z]{2})\-([a-z]{2})', line)
            computer_a, computer_b = match.group(1), match.group(2)
            graph[computer_a].add(computer_b)
            graph[computer_b].add(computer_a)
        return graph 
    

    @read_input("lines")
    def part1(self, lines: list[str]) -> int:
        """
        Algorithm here taken from Arboricity and Subgraph Listing Algorithms
        (Chiba & Nishizeki, 1985).
        """
        graph = self.setup(lines)
        return sum(
            any(vertex.startswith("t") for vertex in triangle)
            for triangle in triangles(graph)
        )


    @read_input("lines")
    def part2(self, lines: list[str]) -> str:
        graph = self.setup(lines)
        largest_clique = max(
            maximal_cliques(graph),
            key=len
        )
        return ','.join(
            computer for computer in sorted(largest_clique)
        )


if __name__=="__main__":
    #solver = Day23("example23.txt")
    solver = Day23("input23.txt")
    print(solver.part1()) # type: ignore
    print(solver.part2()) # type: ignore
