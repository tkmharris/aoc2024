import pytest
from solutions.day23 import Day23
from utils.solutions import solution

@pytest.fixture
def example_solver():
    return Day23("example23.txt")

def puzzle_solver():
    return Day23("input23.py")

def test_example_part1(example_solver):
    result = example_solver.part1()
    expected = solution(23, "example", 1)
    assert result == expected

def test__example_part2(example_solver):
    result = example_solver.part2()
    expected = solution(23, "example", 2)
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = solution(23, "puzzle", 1)
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = solution(23, "puzzle", 2)
    assert result == expected
