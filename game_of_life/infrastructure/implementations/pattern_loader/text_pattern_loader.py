import os
from typing import Set

from game_of_life.domain.position import Position
from game_of_life.infrastructure.interfaces.pattern_loader import PatternLoader


class PlainTextPatternLoader(PatternLoader):
    """Loader for plain text patterns."""

    def load(self, source: str) -> Set[Position]:
        """Load pattern from plain text format.

        Format: '.' or ' ' for dead cells, 'O' or '*' for alive cells

        Args:
            source: Plain text string or file path

        Returns:
            Set of alive cell positions
        """
        alive_cells = set()

        # Check if source is a file path
        if os.path.isfile(source):
            with open(source, 'r') as f:
                lines = f.readlines()
        else:
            lines = source.strip().split('\n')

        for row, line in enumerate(lines):
            for col, char in enumerate(line.strip()):
                if char in ['O', '*', '1']:
                    alive_cells.add(Position(row, col))

        return alive_cells
