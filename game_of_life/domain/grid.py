from dataclasses import dataclass
from typing import Set

from game_of_life.domain.cell_state import CellState
from game_of_life.domain.position import Position


@dataclass
class Grid:
    """Represents the game grid with configurable size.

    Attributes:
        width: Width of the grid
        height: Height of the grid
        alive_cells: Set of positions containing alive cells
    """
    width: int
    height: int
    alive_cells: Set[Position]

    def is_valid_position(self, pos: Position) -> bool:
        """Check if a position is within grid bounds.

        Args:
            pos: Position to check

        Returns:
            True if position is valid, False otherwise
        """
        return 0 <= pos.row < self.height and 0 <= pos.col < self.width

    def get_cell_state(self, pos: Position) -> CellState:
        """Get the state of a cell at given position.

        Args:
            pos: Position to check

        Returns:
            CellState.ALIVE if cell is alive, CellState.DEAD otherwise
        """
        return CellState.ALIVE if pos in self.alive_cells else CellState.DEAD

    def count_alive_neighbors(self, pos: Position) -> int:
        """Count alive neighbors for a given position.

        Uses efficient set lookup for O(1) neighbor checking.

        Args:
            pos: Position to check neighbors for

        Returns:
            Number of alive neighbors (0-8)
        """
        count = 0
        for neighbor_pos in pos.get_neighbors():
            if self.is_valid_position(neighbor_pos) and neighbor_pos in self.alive_cells:
                count += 1
        return count

    def get_all_positions_to_check(self) -> Set[Position]:
        """Get all positions that need to be checked in next generation.

        Optimization: Only check alive cells and their neighbors.

        Returns:
            Set of positions to evaluate
        """
        positions_to_check = set()
        for alive_pos in self.alive_cells:
            positions_to_check.add(alive_pos)
            for neighbor in alive_pos.get_neighbors():
                if self.is_valid_position(neighbor):
                    positions_to_check.add(neighbor)
        return positions_to_check


