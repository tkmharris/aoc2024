import pytest
from solutions.day15 import Day15
from utils.solutions import solution

@pytest.fixture
def example1_solver():
    return Day15("example15_1.txt")

@pytest.fixture
def example2_solver():
    return Day15("example15_2.txt")

@pytest.fixture
def puzzle_solver():
    return Day15("input15.py")

def test_example1_part1(example1_solver):
    result = example1_solver.part1()
    expected = solution(15, "example_1", 1)
    assert result == expected

def test__example1_part2(example1_solver):
    result = example1_solver.part2()
    expected = solution(15, "example_1", 2)
    assert result == expected

def test_example2_part1(example2_solver):
    result = example2_solver.part1()
    expected = solution(15, "example_2", 1)
    assert result == expected

def test__example2_part2(example2_solver):
    result = example2_solver.part2()
    expected = solution(15, "example_2", 2)
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = solution(15, "puzzle", 1)
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = solution(15, "puzzle", 2)
    assert result == expected
