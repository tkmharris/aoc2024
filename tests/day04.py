import pytest
from solutions.day04 import Day04

@pytest.fixture
def puzzle_solver():
    return Day04("input04.py")

def test_example_part1():
    result = Day04("example04.txt").part1()
    expected = 18
    assert result == expected

def test__example_part2():
    result = Day04("example04.txt").part1()
    expected = 9
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = 2591
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = 1880
    assert result == expected
