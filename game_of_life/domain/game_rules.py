from abc import ABC, abstractmethod


class GameRules(ABC):
    @staticmethod
    @abstractmethod
    def should_cell_live(is_alive: bool, neighbor_count: int) -> bool:
        pass


class StandardRules(GameRules):
    """Encapsulates Conway's Game of Life rules."""

    @staticmethod
    def should_cell_live(is_alive: bool, neighbor_count: int) -> bool:
        """
        Determine if a cell should be alive in next generation.

        Conway's Rules:
        1. Any living cell with 2 or 3 neighbors survives
        2. Any dead cell with exactly 3 neighbors becomes alive
        3. All other cells die or stay dead

        Args:
            is_alive: Current state of the cell
            neighbor_count: Number of alive neighbors

        Returns:
            True if cell should be alive, False otherwise
        """
        if is_alive:
            return neighbor_count in [2, 3]
        else:
            return neighbor_count == 3
