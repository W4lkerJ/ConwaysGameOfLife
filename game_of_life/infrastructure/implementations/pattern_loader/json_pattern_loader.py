import json
import os
from typing import Set

from game_of_life.domain.position import Position
from game_of_life.infrastructure.interfaces.pattern_loader import PatternLoader


class JSONPatternLoader(PatternLoader):
    """Loader for JSON format patterns."""

    def load(self, source: str) -> Set[Position]:
        """Load pattern from JSON format.

        Format: {"alive_cells": [[row, col], ...]}

        Args:
            source: JSON string or file path

        Returns:
            Set of alive cell positions
        """
        # Check if source is a file path
        if os.path.isfile(source):
            with open(source, 'r') as f:
                data = json.load(f)
        else:
            data = json.loads(source)

        alive_cells = set()
        for row, col in data.get('alive_cells', []):
            alive_cells.add(Position(row, col))

        return alive_cells
