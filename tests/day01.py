import pytest
from solutions.day01 import Day1

@pytest.fixture
def example_solver():
    return Day1("example01.txt")

@pytest.fixture
def puzzle_solver():
    return Day1("input01.py")

def test_example_part1(example_solver):
    result = example_solver.part1()
    expected = 11
    assert result == expected

def test__example_part2(example_solver):
    result = example_solver.part2()
    expected = 31
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = 2756096
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = 23117829
    assert result == expected
