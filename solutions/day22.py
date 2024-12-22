from utils.solver import Solver
from utils.input import read_input


def last24_bits(number: int):
    bitmask = (1 << 24) - 1
    return number & bitmask


def advance_secret(secret: int, rounds: int = 1) -> int:
    def advance_one(secret):
        secret = last24_bits((secret << 6) ^ secret)
        secret = last24_bits((secret >> 5) ^ secret)
        secret = last24_bits((secret << 11) ^ secret)
        return secret
    
    for _ in range(rounds):
        secret = advance_one(secret)
    
    return secret


class Day22(Solver):
    @read_input("lines")
    def part1(self, lines) -> int:
        secrets = [int(line) for line in lines]
        return sum(
            advance_secret(secret, 2000)
            for secret in secrets
        )


    @read_input("lines")
    def part2(self, lines) -> int:
        pass
    

if __name__=="__main__":
    #solver = Day22("example22.txt")
    solver = Day22("input22.txt")
    print(solver.part1()) # type: ignore
    print(solver.part2()) # type: ignore