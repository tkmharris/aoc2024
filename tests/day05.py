import pytest
from solutions.day05 import Day05

@pytest.fixture
def puzzle_solver():
    return Day05("input05.py")

def test_example_part1():
    result = Day05("example05.txt").part1()
    expected = 143
    assert result == expected

def test__example_part2():
    result = Day05("example05.txt").part1()
    expected = 123
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = 4814
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = 5448
    assert result == expected
