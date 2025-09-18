from abc import ABC, abstractmethod
from typing import Set

from game_of_life.domain.position import Position


class PatternLoader(ABC):
    """Abstract base class for pattern loaders."""

    @abstractmethod
    def load(self, source: str) -> Set[Position]:
        """Load a pattern from a source.

        Args:
            source: Source to load pattern from

        Returns:
            Set of positions with alive cells
        """
        pass
