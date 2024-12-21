import pytest
from solutions.day20 import Day20
from utils.solutions import solution

@pytest.fixture
def example_solver():
    return Day20("example20.txt", savings_required=50)

def puzzle_solver():
    return Day20("input20.py", savings_required=100)

def test_example_part1(example_solver):
    result = example_solver.part1()
    expected = solution(20, "example", 1)
    assert result == expected

def test__example_part2(example_solver):
    result = example_solver.part2()
    expected = solution(20, "example", 2)
    assert result == expected

def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = solution(20, "puzzle", 1)
    assert result == expected

def test_puzzle_part2(puzzle_solver):
    result = puzzle_solver.part2()
    expected = solution(20, "puzzle", 2)
    assert result == expected
