import pytest
from solutions.day03 import Day03
from utils.solutions import solution

@pytest.fixture
def puzzle_solver():
    return Day03("input03.py")

def test_example_part1(example_solver):
    result = example_solver.part1()
    expected = solution(3, "example", 1)
    assert result == expected

def test__example_part2(example_solver):
    result = example_solver.part2()
    expected = solution(3, "example", 2)
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = solution(3, "puzzle", 1)
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = solution(3, "puzzle", 2)
    assert result == expected