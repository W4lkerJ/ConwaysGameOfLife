from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Position:
    """Immutable position in the grid.

    Using frozen dataclass for and immutability.
    """
    row: int
    col: int

    def get_neighbors(self) -> List['Position']:
        """Get all 8 neighboring positions.

        Returns:
            List of Position objects representing all 8 neighbors.
        """
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                neighbors.append(Position(self.row + dr, self.col + dc))
        return neighbors
