import os

from game_of_life.domain.grid import Grid
from game_of_life.domain.position import Position
from game_of_life.infrastructure.interfaces.renderer import Renderer


class ConsoleRenderer(Renderer):
    """Renderer for console/terminal output."""

    def __init__(self, alive_char: str = '█', dead_char: str = '·'):
        """Initialize console renderer.

        Args:
            alive_char: Character to represent alive cells
            dead_char: Character to represent dead cells
        """
        self.alive_char = alive_char
        self.dead_char = dead_char

    def clear_screen(self) -> None:
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def render(self, grid: Grid, generation: int) -> None:
        """Render grid to console.

        Args:
            grid: Grid to render
            generation: Current generation number
        """
        self.clear_screen()
        print(f"Generation: {generation}")
        print(f"Alive cells: {len(grid.alive_cells)}")
        print("─" * (grid.width + 2))

        for row in range(grid.height):
            print("│", end="")
            for col in range(grid.width):
                pos = Position(row, col)
                if pos in grid.alive_cells:
                    print(self.alive_char, end="")
                else:
                    print(self.dead_char, end="")
            print("│")

        print("─" * (grid.width + 2))
