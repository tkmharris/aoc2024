import pytest
from solutions.day18 import Day18, Grid
from utils.solutions import solution

@pytest.fixture
def example_solver():
    return Day18("example18.txt")

def puzzle_solver():
    return Day18("input18.py")

def test_example_part1(example_solver):
    result = example_solver.part1(grid=Grid(7, 7), time=12)
    expected = solution(18, "example", 1)
    assert result == expected

def test__example_part2(example_solver):
    result = example_solver.part2(grid=Grid(7, 7))
    expected = solution(18, "example", 2)
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1(grid=Grid(71, 71), time=1024)
    expected = solution(18, "puzzle", 1)
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2(grid=Grid(71, 71))
    expected = solution(18, "puzzle", 2)
    assert result == expected
