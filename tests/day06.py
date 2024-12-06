import pytest
from solutions.day06 import Day06
from utils.solutions import solution

@pytest.fixture
def example_solver():
    return Day06("example06.txt")

def puzzle_solver():
    return Day06("input06.py")

def test_example_part1(example_solver):
    result = example_solver.part1()
    expected = solution(6, "example", 1)
    assert result == expected

def test__example_part2(example_solver):
    result = example_solver.part2()
    expected = solution(6, "example", 2)
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = solution(6, "puzzle", 1)
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = solution(6, "puzzle", 2)
    assert result == expected
