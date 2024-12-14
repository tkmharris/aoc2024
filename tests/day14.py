import pytest
from solutions.day14 import Day14, Grid
from utils.solutions import solution

@pytest.fixture
def example_solver():
    return Day14("example14.txt", grid=Grid(11, 7))

def puzzle_solver():
    return Day14("input14.py", grid=Grid(101, 103))

def test_example_part1(example_solver):
    result = example_solver.part1()
    expected = solution(14, "example", 1)
    assert result == expected

def test__example_part2(example_solver):
    result = example_solver.part2()
    expected = solution(14, "example", 2)
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = solution(14, "puzzle", 1)
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = solution(14, "puzzle", 2)
    assert result == expected
