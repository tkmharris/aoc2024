
from collections import defaultdict
from dataclasses import dataclass, field
import heapq
from typing import TypeVar, Dict, Any, Generic


T = TypeVar('T')


def dijkstra(graph: Dict[T, Dict[T, int]], start: T) -> dict[T, int]:
    # This is a sub-optimal implementation of Dijkstra.
    # If really pressed for performance we could implement
    # a full priority queue with heapq.)
    distances = defaultdict(lambda: float('inf'))
    distances[start] = 0

    @dataclass(order=True)
    class QueueItem(Generic[T]):
        priority: float
        item: T=field(compare=False)
    
    # Use a heap queue of elements [priority, node].
    # We can't update priorities efficiently so we 
    # just keep track of nodes that we have found the 
    # minimum path for already.
    queue = [
        QueueItem(
            priority=(0 if node == start else float('inf')),
            item=node            
        ) for node in graph
    ]
    heapq.heapify(queue)
    
    visited = set()
    
    while queue:
        node = heapq.heappop(queue).item

        # We wouldn't need this if we had a proper priority queue
        if node in visited:
            continue
        else:
            visited.add(node)
        
        for neighbour, edge_distance in graph[node].items():    
            # ditto re the priority queue
            if neighbour in visited:
                continue
            
            if (distance := distances[node] + edge_distance) < distances[neighbour]:
                distances[neighbour] = distance
                heapq.heappush(
                    queue, QueueItem(priority=distance, item=neighbour)
                )

    return distances