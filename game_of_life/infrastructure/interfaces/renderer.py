from abc import ABC, abstractmethod

from game_of_life.domain.grid import Grid


class Renderer(ABC):
    """Abstract base class for rendering the grid."""

    @abstractmethod
    def render(self, grid: Grid, generation: int) -> None:
        """
        Render the current grid state.

        Args:
            grid: Grid to render
            generation: Current generation number
        """
        pass
