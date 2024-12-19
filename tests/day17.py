import pytest
from solutions.day17 import Day17
from utils.solutions import solution

@pytest.fixture
def example_solver():
    return Day17("example17.txt")

def puzzle_solver():
    return Day17("input17.py")

def test_example_part1(example_solver):
    result = example_solver.part1()
    expected = solution(17, "example", 1)
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = solution(17, "puzzle", 1)
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = solution(17, "puzzle", 2)
    assert result == expected
