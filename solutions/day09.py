from dataclasses import dataclass
from utils.solver import Solver
from utils.input import read_input

def swap(lst, i, j):
    lst[i], lst[j] = lst[j], lst[i]

    
class Day09(Solver):
    @read_input("string")
    def part1(self, input_string) -> int: 
        file_blocks = []
        file_mode = True
        id_number = 0
        for block_size in map(int, input_string):
            if file_mode:
                file_blocks.extend([id_number] * block_size)
                id_number += 1
            else:
                file_blocks.extend([None] * block_size)
            file_mode = not file_mode

        left, right = 0, len(file_blocks) - 1
        while left < right:
            if file_blocks[left] is not None:
                left += 1
                continue
            
            if file_blocks[right] is not None:
                file_blocks[left] = file_blocks[right]
                file_blocks[right] = None
                left += 1
                
            right -= 1

        return sum(
            position * value 
            for position, value in enumerate(file_blocks)
            if value is not None
        )

    
    @dataclass
    class Block:
        id: int | None
        starts_at: int
        length: int
    
    @read_input("string")
    def part2(self, input_string) -> int: 
        blocks = []
        blanks = []
        file_mode = True
        id_number = 0
        position = 0
        for block_size in map(int, input_string):
            if file_mode:
                block = self.Block(id=id_number, starts_at=position, length=block_size)
                blocks.append(block)
                id_number += 1
            else:
                block = self.Block(id=None, starts_at=position, length=block_size)
                blanks.append(block)
            
            position += block_size
            file_mode = not file_mode

        for block in blocks[::-1]:
            for blank in blanks:
                if blank.starts_at < block.starts_at and blank.length >= block.length:
                    blanks.append(
                        self.Block(id=None, starts_at=block.starts_at, length=block.length)
                    )
                    block.starts_at = blank.starts_at
                    blank.length -= block.length
                    blank.starts_at += block.length
                    break
        
        filesystem = []
        sorted_blocks = sorted(blocks + blanks, key=lambda block: block.starts_at)
        for block in sorted_blocks:
            filesystem.extend([block.id] * block.length)
            
        return sum(
            position * value 
            for position, value in enumerate(filesystem)
            if value is not None
        )

if __name__=="__main__":
    solver = Day09("input09.txt")
    print(solver.part1())
    print(solver.part2())