from dataclasses import dataclass
from typing import Generator
from utils.solver import Solver
from utils.input import read_input
    
class Day09(Solver):
    def chunks(self, disk_map: list[int]) -> Generator[tuple[int, int]]:
        if len(disk_map) % 2 == 1:
            disk_map.append(0)
        for i in range(0, len(disk_map), 2):
            yield tuple(disk_map[i:i + 2])


    def checksum(self, filesystem: list[int | None]) -> int:
        return sum(
            position * value 
            for position, value in enumerate(filesystem)
            if value is not None
        )
    

    @read_input("string")
    def part1(self, input_string: str) -> int: 
        disk_map = list(map(int, input_string))
        filesystem = []
        
        for file_id, (block_size, blank_size) in enumerate(self.chunks(disk_map)):
            filesystem.extend([file_id] * block_size)
            filesystem.extend([None] * blank_size)

        left, right = 0, len(filesystem) - 1
        while left < right:
            if filesystem[left] is not None:
                left += 1
                continue
            
            if filesystem[right] is not None:
                filesystem[left] = filesystem[right]
                filesystem[right] = None
                left += 1
                
            right -= 1

        return self.checksum(filesystem)
    
    
    @read_input("string")
    def part2(self, input_string) -> int: 
        # For storing details of file/blank block.
        @dataclass
        class Block:
            id: int | None
            starts_at: int
            size: int
        
        # Create arrays of file blocks and blank blocks from input.
        disk_map = list(map(int, input_string))
        filesystem_position = 0
        file_blocks = []
        blank_blocks = []
        
        for file_id, (block_size, blank_size) in enumerate(self.chunks(disk_map)):
            file_blocks.append(
                Block(id=file_id, starts_at=filesystem_position, size=block_size)
            )
            blank_blocks.append(
                Block(id=None, starts_at=filesystem_position + block_size, size=blank_size)
            )
            filesystem_position += (block_size + blank_size)
        
        # Move file blocks earlier where possible.
        for block in file_blocks[::-1]:
            for blank in blank_blocks:
                if blank.starts_at < block.starts_at and blank.size >= block.size:
                    blank_blocks.append(
                        Block(id=None, starts_at=block.starts_at, size=block.size)
                    )
                    block.starts_at = blank.starts_at
                    blank.size -= block.size
                    blank.starts_at += block.size
                    break
        
        # Build filesystem layout from blocks and blanks.
        filesystem = []
        for block in sorted(file_blocks + blank_blocks, key=lambda block: block.starts_at):
            filesystem.extend([block.id] * block.size)
            
        return self.checksum(filesystem)


if __name__=="__main__":
    solver = Day09("input09.txt")
    print(solver.part1())
    print(solver.part2())