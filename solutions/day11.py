from functools import lru_cache
from utils.solver import Solver
from utils.input import read_input
from collections import defaultdict

@lru_cache
def offspring(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        half_length = len(str(stone)) // 2
        left, right = int(str(stone)[:half_length]), int(str(stone)[half_length:])
        return [left, right]
    else:
        return [stone * 2024]
    
def blink(stone_counts: dict[int, int]) -> dict[int, int]:
    new_stones = defaultdict(int)
    for stone, count in stone_counts.items():
        for new_stone in offspring(stone):
            new_stones[new_stone] += count
    return new_stones

def count_stones(initial_values, generations):
    stones = {value: 1 for value in initial_values}
    for _ in range(generations):
        stones = blink(stones)
    return sum(
        number_of_stones for _, number_of_stones in stones.items()
    )
    
class Day11(Solver):
    @read_input("string")
    def part1(self, input_string: str) -> int: 
        initial_values = map(int, input_string.split())
        return count_stones(initial_values, 25)

    @read_input("string")
    def part2(self, input_string: str) -> int: 
        initial_values = map(int, input_string.split())
        return count_stones(initial_values, 75)

if __name__=="__main__":
    solver = Day11("input11.txt")
    print(solver.part1())
    print(solver.part2())