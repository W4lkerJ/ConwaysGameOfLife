from game_of_life.domain.cell_state import CellState
from game_of_life.domain.grid import Grid
from game_of_life.domain.game_rules import GameRules


class GameEngine:
    """Core game engine implementing the simulation logic."""

    def __init__(self, rules: GameRules = None):
        """Initialize the game engine.

        Args:
            rules: Game rules to use (defaults to standard Conway rules)
        """
        self.rules = rules or GameRules()

    def compute_next_generation(self, grid: Grid) -> Grid:
        """Compute the next generation of the grid.

        Optimized algorithm that only checks relevant cells.

        Args:
            grid: Current grid state

        Returns:
            New Grid object representing next generation
        """
        new_alive_cells = set()

        # Only check cells that could possibly change
        for pos in grid.get_all_positions_to_check():
            is_alive = grid.get_cell_state(pos) == CellState.ALIVE
            neighbor_count = grid.count_alive_neighbors(pos)

            if self.rules.should_cell_live(is_alive, neighbor_count):
                new_alive_cells.add(pos)

        return Grid(grid.width, grid.height, new_alive_cells)
