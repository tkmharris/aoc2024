import pytest
from solutions.day02 import Day02
from utils.solutions import solution

@pytest.fixture
def example_solver():
    return Day02("example02.txt")

@pytest.fixture
def puzzle_solver():
    return Day02("input02.py")

def test_example_part1(example_solver):
    result = example_solver.part1()
    expected = solution(2, "example", 1)
    assert result == expected

def test__example_part2(example_solver):
    result = example_solver.part2()
    expected = solution(2, "example", 2)
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = solution(2, "puzzle", 1)
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = solution(2, "puzzle", 2)
    assert result == expected