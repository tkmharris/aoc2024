"""
NOTES:
This is likely not the best way to do this. 
I skipped the following crucial line while reading the problem:
> Because the first update does not include some page numbers, the ordering rules 
> involving those missing page numbers are ignored.
So I thought all constraints (and all constraints that can be derived from them)
applied to _every_ update and settled on tracking the partial order with a tree
(actually forest) structure and defining an order relation by looking for a node
in another node's descendants. 
After getting the wrong answer with that I noticed the above line. But I didn't have 
the heart to start from scratch so now I build a little partial ordering tree for
_each_ update using only the relevant constraints. 
"""

import re
from collections import deque
from functools import lru_cache
from itertools import product
from utils.solver import Solver
from utils.input import read_input

class Page:
    def __init__(self, value):
        self.value = value
        self.children = set()

    def add_child(self, child):
        self.children.add(child)

    # We won't call descendants until after we've built the trees
    # we'll use these pages in, so it's safe to memoize this.
    @lru_cache(maxsize=None)
    def descendants(self):
        descendants = set()
        stack = deque([self])
        while stack:
            page = stack.pop()
            for child in page.children:
                if child not in descendants:
                    descendants.add(child)
                    stack.append(child)
        return descendants

    def __gt__(self, other):
        return self in other.descendants()
    

class Day05(Solver):
    def get_constraints_and_updates(self, lines):
        constraints = []
        updates = []
        for line in lines:
            if match := re.match(r'(\d+)\|(\d+)', line):
                constraints.append((int(match.group(1)), int(match.group(2))))
            elif match := re.match(r'(\d+)(,\d+)*', line):
                updates.append([int(num) for num in line.split(',')])
        return constraints, updates

    @read_input("lines")
    def part1(self, lines) -> int:
        constraints, updates = self.get_constraints_and_updates(lines)

        def is_valid(update):
            # build constraint tree
            pages = {number: Page(number) for number in update}
            for constraint in constraints:
                if constraint in product(update, update):
                    first_page, second_page = pages[constraint[0]], pages[constraint[1]]
                    first_page.add_child(second_page)

            # validate update with tree
            return all(
                not (pages[update[i - 1]] > pages[update[i]])
                for i in range(1, len(update))
            )
        
        return sum(
            update[len(update) // 2] 
            for update in filter(is_valid, updates)
        )        


    @read_input("lines")
    def part2(self, lines) -> int:
        constraints, updates = self.get_constraints_and_updates(lines)

        def sort_if_invalid(update):
            # build constraint tree
            pages = {number: Page(number) for number in update}
            for constraint in constraints:
                if constraint in product(update, update):
                    first_page, second_page = pages[constraint[0]], pages[constraint[1]]
                    first_page.add_child(second_page)
            
            # use tree to check for validity and sort otherwise
            if any(
                (pages[update[i - 1]] > pages[update[i]])
                for i in range(1, len(update))
            ):
                return sorted(pages.values())

        result = 0
        for update in updates:
            if sorted_update := sort_if_invalid(update):
                result += sorted_update[len(sorted_update) // 2].value
        
        return result


if __name__=="__main__":
    solver = Day05("input05.txt")
    print(solver.part1())
    print(solver.part2())