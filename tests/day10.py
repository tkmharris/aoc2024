import pytest
from solutions.day10 import Day10
from utils.solutions import solution

@pytest.fixture
def example_solver():
    return Day10("example10.txt")

def puzzle_solver():
    return Day10("input10.py")

def test_example_part1(example_solver):
    result = example_solver.part1()
    expected = solution(10, "example", 1)
    assert result == expected

def test__example_part2(example_solver):
    result = example_solver.part2()
    expected = solution(10, "example", 2)
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = solution(10, "puzzle", 1)
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = solution(10, "puzzle", 2)
    assert result == expected
