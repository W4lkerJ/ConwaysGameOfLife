from typing import Set

from game_of_life.domain.position import Position
from game_of_life.infrastructure.interfaces.pattern_loader import PatternLoader


class PlainTextPatternLoader(PatternLoader):
    """Loader for plain text patterns."""

    def __init__(self, source: str):
        """
        Load pattern from plain text given as string.

        Format: '.' or '0' for dead cells, '1' or '*' for alive cells

        Args:
            source: Plain text string containing the start configuration
        """

        self.source = source

        self._alive_chars = ["1", "*"]
        self._dead_chars = ["0", "·"]

    def load(self) -> Set[Position]:
        """
        Load pattern from set plain text format.

        Returns:
            Set of alive cell positions
        """
        alive_cells = set()

        lines = self.source.strip().split('\n')

        for row, line in enumerate(lines):
            for col, char in enumerate(line.strip()):
                # Guard to catch invalid pattern characters
                if char not in self._dead_chars and char not in self._alive_chars:
                    raise ValueError(f"Loaded char {char} is not a valid pattern character. Please use 0, 1")

                # Check, if cell is configured alive
                if char in self._alive_chars:
                    alive_cells.add(Position(row, col))

        return alive_cells
