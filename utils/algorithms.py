
from collections import defaultdict, deque
from dataclasses import dataclass, field
import heapq
from typing import TypeVar, Dict, List, Generic


T = TypeVar('T')


def bfs_distance(
        graph: Dict[T, List[T]],
        start: T,
        end: T | None = None,
    ) -> Dict[T, int] | int | None:

    distances = defaultdict(int)
    distances[start] = 0
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        
        for neighbour in graph[node]:
            
            if distances[neighbour] > 0:
                continue
            
            distances[neighbour] = distances[node] + 1
            if neighbour not in queue:
                queue.append(neighbour)

        if end and distances[end] > 0:
            return distances[end]
    
    if not end:
        return distances
    return None
    


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
