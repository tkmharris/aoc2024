import pytest
from solutions.day02 import Day2

@pytest.fixture
def example_solver():
    return Day2("example02.txt")

@pytest.fixture
def puzzle_solver():
    return Day2("input02.py")

def test_example_part1(example_solver):
    result = example_solver.part1()
    expected = 2
    assert result == expected

def test__example_part2(example_solver):
    result = example_solver.part2()
    expected = 4
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = 411
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = 465
    assert result == expected
