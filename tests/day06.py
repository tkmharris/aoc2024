import pytest
from solutions.day06 import Day06

@pytest.fixture
def puzzle_solver():
    return Day06("input06.py")

def test_example_part1():
    result = Day06("example06.txt").part1()
    expected = 41
    assert result == expected

def test__example_part2():
    result = Day06("example06.txt").part1()
    expected = 6
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = 4663
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = 1530
    assert result == expected
