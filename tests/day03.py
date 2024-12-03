import pytest
from solutions.day03 import Day03

@pytest.fixture
def puzzle_solver():
    return Day03("input03.py")

def test_example_part1():
    result = Day03("example03_1.txt").part1()
    expected = 161
    assert result == expected

def test__example_part2():
    result = Day03("example03_2.txt").part1()
    expected = 48
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = 164730528
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = 70478672
    assert result == expected
