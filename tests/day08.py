import pytest
from solutions.day08 import Day08
from utils.solutions import solution

@pytest.fixture
def example_solver():
    return Day08("example08.txt")

def puzzle_solver():
    return Day08("input08.py")

def test_example_part1(example_solver):
    result = example_solver.part1()
    expected = solution(8, "example", 1)
    assert result == expected

def test__example_part2(example_solver):
    result = example_solver.part2()
    expected = solution(8, "example", 2)
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = solution(8, "puzzle", 1)
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = solution(8, "puzzle", 2)
    assert result == expected
