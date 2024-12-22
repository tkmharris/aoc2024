import pytest
from solutions.day22 import Day22
from utils.solutions import solution

@pytest.fixture
def example_solver():
    return Day22("example22.txt", savings_required=50)


def test_example_part1(example_solver):
    result = example_solver.part1()
    expected = solution(22, "example", 1)
    assert result == expected


def test_puzzle_part1(puzzle_solver):
    result = puzzle_solver.part1()
    expected = solution(22, "puzzle", 1)
    assert result == expected
