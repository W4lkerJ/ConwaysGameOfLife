import json
import os
from typing import Set

from game_of_life.domain.position import Position
from game_of_life.infrastructure.interfaces.pattern_loader import PatternLoader


class JSONPatternLoader(PatternLoader):
    """
    Loader for JSON format patterns.

    Format: {"alive_cells": [[row, col], ...]}

    """

    def __init__(self, json_source: str):
        self.json_source = json_source

    def load(self) -> Set[Position]:
        """Load pattern from JSON format.

        Returns:
            Set of alive cell positions
        """

        data = json.loads(self.json_source)

        if "alive_cells" not in data:
            raise ValueError("Loaded json pattern does not contain 'alive_cells'")

        alive_cells = set()
        for row, col in data['alive_cells']:
            alive_cells.add(Position(row, col))

        return alive_cells
